from flask import Blueprint, jsonify
from flask_login import current_user, login_required
from flask_restful import reqparse
from data.rest.rest_utils import assert_account_type
from data.db import db_sessionmaker
from data.db.models.doctor import Doctor


blueprint = Blueprint(
    'recover',
    __name__,
    template_folder='templates'
)


@blueprint.route('/recover/patient/', methods=['POST'])
@blueprint.route('/recover/patient', methods=['POST'])
def recover_patient():
    ("""Восстановление пароля пациента"""
     """по электронной почте(адрес в поле login)""")
    # TODO email api
    return jsonify(success='OK')


recover_doctor_request_parser = reqparse.RequestParser()
recover_doctor_request_parser.add_argument('id', required=False, type=int)
recover_doctor_request_parser.add_argument('login', required=False)
recover_doctor_request_parser.add_argument('password', required=True)


@blueprint.route('/recover/doctor/', methods=['POST'])
@blueprint.route('/recover/doctor', methods=['POST'])
@login_required
def recover_doctor():
    """Изменение пароля доктора администратором"""
    assert_account_type('Admin')
    args = recover_doctor_request_parser.parse_args()
    if args['id'] is not None:
        search_by = 'id'
    elif args['login'] is not None:
        search_by = 'login'
    else:
        return jsonify(error='Укажите айди доктора или его логин'), 400
    db_sess = db_sessionmaker.create_session()
    doctor = db_sess.query(Doctor).filter_by(
        **{search_by: args[search_by]}).first()
    if doctor is None or doctor.clinic_id != current_user.clinic_id:
        return jsonify(error=(
            f'Доктор с {search_by}={args[search_by]} '
            'в Вашей поликлинике не найден')), 404
    doctor.set_password(args['password'])
    db_sess.commit()
    return jsonify(success='OK')
