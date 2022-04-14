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
    return render_template('MainForm.html', user=user, qui={'Кровосток': 'https://genius.com/albums/Krovostok/Blood-river',
    'Градиент': 'https://uigradients.com/#Quepal',
    'Словари': 'https://pythonworld.ru/tipy-dannyx-v-python/slovari-dict-funkcii-i-metody-slovarej.html',
    'Слайд': 'https://www.avito.ru/kazan/muzykalnye_instrumenty/slayd_keramicheskiy_dlya_gitary_2312251328?slocation=621585',
    'Мафия': 'https://www.youtube.com/watch?v=B0veWDpV46c',
    'Daughter - All I Wanted': 'https://www.youtube.com/watch?v=isges2l3qaY'},
    type='Список анкет')
