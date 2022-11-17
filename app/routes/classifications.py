import redis
from flask import render_template
from rq import Connection, Queue
from rq.job import Job

from app import app
from app.forms.classification_form import ClassificationForm
from ml.classification_utils import classify_image
from config import Configuration

config = Configuration()


@app.route('/classifications', methods=['GET', 'POST'])
def classifications():
    """API for selecting a model and an image and running a 
    classification job. Returns the output scores from the 
    model."""
    form = ClassificationForm()
    if form.validate_on_submit():  # POST
        image_id = form.image.data
        model_id = form.model.data
        # TODO create the result_dict, with a key 'data' that stores
        #  the output of the classification function

        redis_url = config.REDIS_URL
        redis_connection = redis.from_url(redis_url)
        with Connection(redis_connection):
            q = Queue(name=config.QUEUE)
        job = Job.create(classify_image,
                         kwargs=dict(model_id=model_id,
                                     img_id=image_id))
        task = q.enqueue_job(job)
        return render_template('classification_output_queue.html', image_id = image_id,
                   jobID = task.get_id())
        #clf_output = classify_image(model_id=model_id, img_id=image_id)
        #result = dict(data=clf_output)


        # returns the image classification output from the specified model
        #return render_template('classification_output.html', image_id=image_id, results=result)

    # otherwise, it is a get request and should return the
    # image and model selector
    return render_template('classification_select.html', form=form)
