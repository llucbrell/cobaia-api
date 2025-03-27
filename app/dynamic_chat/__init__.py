from flask import Blueprint

dynamic_chat = Blueprint('dynamic_chat', __name__)

from . import views
