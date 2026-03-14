from flask import Blueprint

inscribir = Blueprint(
    'inscribir',
    __name__,
    template_folder='templates',
    static_folder='static'
)

from . import routes
