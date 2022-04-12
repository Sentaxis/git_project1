from flask import Blueprint, redirect, render_template
import flask_login

from data.db import db_sessionmaker  # импорт бд
from data.db.models.admin import Admin
from data.db.models.doctor import Doctor
from data.db.models.patient import Patient

blueprint = Blueprint(
    'interface',
    __name__,
    template_folder='templates'
)


@blueprint.route('/', methods=['GET'])
def index():
    user =  flask_login.current_user
    if user.is_anonymous:
        user = None
    return render_template('MainForm.html', user=user)
