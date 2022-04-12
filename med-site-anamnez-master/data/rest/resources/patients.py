from flask import Blueprint, session, jsonify
from flask_restful import reqparse
from flask_login import current_user, login_required
from data.db.models.patient import Patient
from data.db.models.clinic import Clinic
from data.db import db_sessionmaker
from data.rest.rest_utils import \
    abort_if_model_not_found, assert_account_type, \
    abort_if_user_exists, get_required_strs_args_names, \
    abort_if_blank_str_in_args, strip_strs_in_args
from data import req_manager


blueprint = Blueprint(
    'patients_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/patients/<int:patient_id>/', methods=['GET'])
@blueprint.route('/api/patients/<int:patient_id>', methods=['GET'])
@login_required
def get_one_patient(patient_id: int):
    verdict = assert_account_type(['Doctor', 'Patient', 'Admin'])
    if verdict is not None:
        return verdict
    verdict = abort_if_model_not_found(Patient, patient_id)
    if verdict is not None:
        return verdict
    db_sess = db_sessionmaker.create_session()
    patient = db_sess.query(Patient).get(patient_id)
    if (session['account_type'] == 'Patient' and
            current_user.id != patient_id) or (
                session['account_type'] in ('Doctor', 'Admin') and
            current_user.clinic_id != patient.clinic_id):
        return jsonify(error='Вам запрещено совершать это действие'), 403
    return jsonify(patient=patient.to_dict()), 200


@blueprint.route('/api/patients/<int:patient_id>/', methods=['DELETE'])
@blueprint.route('/api/patients/<int:patient_id>', methods=['DELETE'])
@login_required
def delete_one_patient(patient_id: int):
    verdict = assert_account_type('Admin')
    if verdict is not None:
        return verdict
    verdict = abort_if_model_not_found(Patient, patient_id)
    if verdict is not None:
        return verdict
    db_sess = db_sessionmaker.create_session()
    patient = db_sess.query(Patient).get(patient_id)
    if current_user.clinic_id != patient.clinic_id:
        return jsonify(error='Вам запрещено совершать это действие'), 403
    db_sess.query(Patient).filter_by(id=patient_id).delete()
    db_sess.commit()
    return jsonify(success='OK'), 200


@blueprint.route('/api/patients/', methods=['GET'])
@blueprint.route('/api/patients', methods=['GET'])
@login_required
def get_patients():
    verdict = assert_account_type(['Doctor', 'Admin'])
    if verdict is not None:
        return verdict
    pinned_patients = current_user.clinic.patients
    pinned_patients = tuple(ptnt.to_dict() for ptnt in pinned_patients)
    return jsonify(patients=pinned_patients), 200


patient_request_parser = reqparse.RequestParser()
patient_request_parser.add_argument('login', required=True, type=str)
patient_request_parser.add_argument('password', required=True, type=str)
patient_request_parser.add_argument('surname', required=True, type=str)
patient_request_parser.add_argument('name', required=True, type=str)
patient_request_parser.add_argument('patronymic', required=True, type=str)
patient_request_parser.add_argument('clinic_id', required=True, type=int)


@blueprint.route('/api/patients/', methods=['POST'])
@blueprint.route('/api/patients', methods=['POST'])
def create_patient():
    parser_request = req_manager.get_request('POST')
    args = patient_request_parser.parse_args(req=parser_request)
    verdict = abort_if_model_not_found(Clinic, args['clinic_id'])
    if verdict is not None:
        return verdict
    required_strs_args = get_required_strs_args_names(
        patient_request_parser.args)
    strip_strs_in_args(args, required_strs_args)
    verdict = abort_if_blank_str_in_args(
        args, required_strs_args)
    if verdict is not None:
        return verdict
    verdict = abort_if_user_exists(user_login=args['login'])
    if verdict is not None:
        return verdict
    db_sess = db_sessionmaker.create_session()
    patient = Patient(login=args['login'],
                      passwd_hash='',
                      surname=args['surname'],
                      name=args['name'],
                      patronymic=args['patronymic'],
                      clinic_id=args['clinic_id'])
    patient.set_password(args['password'])
    db_sess.add(patient)
    db_sess.commit()
    return jsonify(success='OK'), 200
