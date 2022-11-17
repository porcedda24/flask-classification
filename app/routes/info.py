from app import app
from app.utils.list_images import list_images
from config import Configuration
conf = Configuration()

@app.route('/info', methods=['GET'])
def info():
    """Returns a dictionary with the list of models and
    the list of available image files."""
    data = dict()
    data['models'] = conf.models
    data['images'] = list_images()
    return data
