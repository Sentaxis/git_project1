from email import message
from flask import Blueprint, session, jsonify, render_template, redirect, request
from flask_restful import reqparse
from flask_login import LoginManager, \
    login_user, logout_user, login_required, current_user
from data.db import db_sessionmaker
from data.db.models.admin import Admin
from data.db.models.doctor import Doctor
from data.db.models.patient import Patient
from data.db.__all_models import USER_MODELS
from data import req_manager

from .flask_wtf_forms import LoginForm, RegisterForm, RegisterDoctorForm, \
                            RegisterClinicForm, RegisterModeratorForm

from . import req_manager
from .rest.resources.doctors import create_doctor
from .rest.resources.patients import create_patient
from .rest.resources.clinics import get_clinics


def register_login_manager(app):
    ("""Настраивает login manager. """
     """Перед регистрацией blueprint'а """
     """нужно вызвать эту функцию """
     """с экземпляром приложения Flask""")
    login_manager = LoginManager(app)

    @login_manager.user_loader
    def load_user(user_id: int):
        account_type = session.get('account_type')
        if account_type == 'Patient':
            model = Patient
        elif account_type == 'Doctor':
            model = Doctor
        elif account_type == 'Admin':
            model = Admin
        else:
            return None
        try:
            user_id = int(user_id)
        except TypeError:
            return None
        except ValueError:
            return None
        db_sess = db_sessionmaker.create_session()
        return db_sess.query(model).get(user_id)


blueprint = Blueprint(
    'auth',
    __name__,
    template_folder='templates'
)


login_request_parser = reqparse.RequestParser()
login_request_parser.add_argument('login', required=True)
login_request_parser.add_argument('password', required=True)


@blueprint.route('/api/login/', methods=['POST'])
@blueprint.route('/api/login', methods=['POST'])
def login_api():
    args = login_request_parser.parse_args(req=req_manager.get_request('POST'))
    db_sess = db_sessionmaker.create_session()
    for model in USER_MODELS:
        user = db_sess.query(model).filter_by(login=args['login']).first()
        if user is not None:
            break
    else:
        return jsonify(error='Неправильный логин'), 400
    if not user.check_password(args['password']):
        return jsonify(error='Неправильный пароль'), 400
    session['account_type'] = model.__name__.capitalize()
    login_user(user)
    return jsonify(success='OK'), 200


@blueprint.route('/api/logout/', methods=['POST'])
@blueprint.route('/api/logout', methods=['POST'])
def logout_api():
    if 'account_type' in session:
        del session['account_type']
    logout_user()
    return jsonify(success='OK'), 200


@blueprint.route('/login/', methods=["GET", "POST"])
@blueprint.route('/login', methods=["GET", "POST"])
def login():
    user =  current_user
    if not user.is_anonymous:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        req_manager.set_json({'login': form.login.data,
                              'password': form.password.data})
        mess, code = login_api()
        if code == 200:
            return redirect('/')
        else:
            return render_template('LoginForm.html', form=form, message=mess.json['error'])
    return render_template('LoginForm.html', form=form)


@blueprint.route('/register', methods=["GET", "POST"])
def register():
    user =  current_user
    if not user.is_anonymous:
        return redirect('/')
    form = RegisterForm()
    clinics, s_code = get_clinics()
    if form.validate_on_submit():
        req_manager.set_json({'login': form.login.data,
                              'password': form.password.data,
                              'name': form.name.data,
                              'surname': form.surname.data,
                              'patronymic': form.patronymic.data,
                              'clinic_id': request.form.get('clinic')})
        mess, code = create_patient()
        if code == 200:
            return redirect('/')
        else:
            return render_template('RegisterForm.html', form=form, hospitails=clinics.json['clinics'], message=mess.json['error'])
    return render_template('RegisterForm.html', form=form, hospitails=clinics.json['clinics'])


#TODO: исправить баг
@blueprint.route('/doctor_register', methods=["GET", "POST"])
@login_required
def doctor_register():
    user =  current_user
    if user.__class__.__name__ != 'Admin':
        return redirect('/')
    form = RegisterDoctorForm()
    if form.validate_on_submit():
        req_manager.set_json({'login': form.login.data,
                              'password': form.password.data,
                              'name': form.name.data,
                              'surname': form.surname.data,
                              'patronymic': form.patronymic.data,
                              'clinic_id': user.clinic_id})
        mess, code = create_doctor()
        if code == 200:
            return redirect('/')
        else:
            return render_template('RegisterDoctorForm.html', form=form, user=user, message=mess.json['error'])
    return render_template('RegisterDoctorForm.html', form=form, user=user)


@blueprint.route('/logout/', methods=['GET', 'POST'])
@blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')
