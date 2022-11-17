import redis
from rq import Connection, Queue

from app import app
from config import Configuration

config = Configuration()


@app.route('/classifications/<string:job_id>', methods=['GET'])
def classifications_id(job_id):
    """Returns the status and the result of the job identified
    by the id specified in the path."""
      # TODO connect to the database and get the task by the id
    redis_url = config.REDIS_URL
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection):
        q = Queue(name=config.QUEUE)
        task = q.fetch_job(job_id)
    response = {
        'task_status': task.get_status(),
        'data': task.result,
    }
    return response
