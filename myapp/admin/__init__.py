from flask import Blueprint

myadmin = Blueprint('myadmin', __name__)

from myapp.admin import routes