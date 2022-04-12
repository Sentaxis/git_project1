from flask import Blueprint, jsonify
from flask_restful import reqparse
from flask_login import current_user, login_required
from data.db.models.doctor import Doctor
from data.db import db_sessionmaker
from data.rest.rest_utils import \
    abort_if_model_not_found, assert_account_type, \
    abort_if_user_exists, get_required_strs_args_names, \
    abort_if_blank_str_in_args, strip_strs_in_args
from data import req_manager


blueprint = Blueprint(
    'doctors_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/doctors/<int:doctor_id>/', methods=['GET'])
@blueprint.route('/api/doctors/<int:doctor_id>', methods=['GET'])
@login_required
def get_one_doctor(doctor_id: int):
    verdict = assert_account_type(['Doctor', 'Admin'])
    if verdict is not None:
        return verdict
    verdict = abort_if_model_not_found(Doctor, doctor_id)
    if verdict is not None:
        return verdict
    db_sess = db_sessionmaker.create_session()
    doctor = db_sess.query(Doctor).get(doctor_id)
    if current_user.clinic_id != doctor.clinic_id:
        return jsonify(error='Вам запрещено совершать это действие'), 403
    return jsonify(doctor=doctor.to_dict()), 200


@blueprint.route('/api/doctors/<int:doctor_id>/', methods=['DELETE'])
@blueprint.route('/api/doctors/<int:doctor_id>', methods=['DELETE'])
@login_required
def delete_one_doctor(doctor_id: int):
    verdict = assert_account_type('Admin')
    if verdict is not None:
        return verdict
    verdict = abort_if_model_not_found(Doctor, doctor_id)
    if verdict is not None:
        return verdict
    db_sess = db_sessionmaker.create_session()
    doctor = db_sess.query(Doctor).get(doctor_id)
    if current_user.clinic_id != doctor.clinic_id:
        return jsonify(error='Вам запрещено совершать это действие'), 403
    db_sess.query(Doctor).filter_by(id=doctor_id).delete()
    db_sess.commit()
    return jsonify(success='OK'), 200


@blueprint.route('/api/doctors/', methods=['GET'])
@blueprint.route('/api/doctors', methods=['GET'])
@login_required
def get_doctors():
    verdict = assert_account_type(['Doctor', 'Admin'])
    if verdict is not None:
        return verdict
    pinned_doctors = current_user.clinic.doctors
    pinned_doctors = tuple(doc.to_dict() for doc in pinned_doctors)
    return jsonify(doctors=pinned_doctors), 200


doctor_request_parser = reqparse.RequestParser()
doctor_request_parser.add_argument('login', required=True, type=str)
doctor_request_parser.add_argument('password', required=True, type=str)
doctor_request_parser.add_argument('surname', required=True, type=str)
doctor_request_parser.add_argument('name', required=True, type=str)
doctor_request_parser.add_argument('patronymic', required=True, type=str)


@blueprint.route('/api/doctors/', methods=['POST'])
@blueprint.route('/api/doctors', methods=['POST'])
@login_required
def create_doctor():
    parser_request = req_manager.get_request('POST')
    verdict = assert_account_type('Admin')
    if verdict is not None:
        return verdict
    required_strs_args = get_required_strs_args_names(
        doctor_request_parser.args)
    args = doctor_request_parser.parse_args(req=parser_request)
    strip_strs_in_args(args, required_strs_args)
    verdict = abort_if_blank_str_in_args(
        args, required_strs_args)
    if verdict is not None:
        return verdict
    verdict = abort_if_user_exists(user_login=args['login'])
    if verdict is not None:
        return verdict
    db_sess = db_sessionmaker.create_session()
    doctor = Doctor(login=args['login'],
                    passwd_hash='',
                    surname=args['surname'],
                    name=args['name'],
                    patronymic=args['patronymic'],
                    clinic_id=current_user.clinic_id)
    doctor.set_password(args['password'])
    db_sess.add(doctor)
    db_sess.commit()
    return jsonify(success='OK'), 200
