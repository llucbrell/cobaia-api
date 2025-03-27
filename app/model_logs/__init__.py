from flask import Blueprint

dynamic_logs = Blueprint('dynamic_logs', __name__)
dynamic_api_logs = Blueprint('dynamic_api_logs', __name__)

from . import views
from . import api
