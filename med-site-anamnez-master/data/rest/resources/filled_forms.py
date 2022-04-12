from flask import Blueprint, jsonify
from flask_restful import reqparse
from flask_login import current_user, login_required
from data.db.models.filled_form import FilledForm
from data.db.models.form import Form
from data.db.models.patient import Patient
from data.db import db_sessionmaker
from data.rest.rest_utils import \
    abort_if_model_not_found, assert_account_type
from data import req_manager


blueprint = Blueprint(
    'filled_forms_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/filled_forms/<int:filled_form_id>/', methods=['GET'])
@blueprint.route('/api/filled_forms/<int:filled_form_id>', methods=['GET'])
@login_required
def get_one_filled_form(filled_form_id: int):
    verdict = assert_account_type(['Doctor', 'Admin'])
    if verdict is not None:
        return verdict
    verdict = abort_if_model_not_found(FilledForm, filled_form_id)
    if verdict is not None:
        return verdict
    db_sess = db_sessionmaker.create_session()
    filled_form = db_sess.query(FilledForm).get(filled_form_id)
    if current_user.clinic_id != filled_form.patient.clinic_id:
        return jsonify(error='Вам запрещено совершать это действие'), 403
    return jsonify(filled_form=filled_form.to_dict()), 200


@blueprint.route('/api/filled_forms/<int:filled_form_id>/', methods=['DELETE'])
@blueprint.route('/api/filled_forms/<int:filled_form_id>', methods=['DELETE'])
@login_required
def delete_one_filled_form(filled_form_id: int):
    verdict = assert_account_type('Admin')
    if verdict is not None:
        return verdict
    verdict = abort_if_model_not_found(FilledForm, filled_form_id)
    if verdict is not None:
        return verdict
    db_sess = db_sessionmaker.create_session()
    filled_form = db_sess.query(FilledForm).get(filled_form_id)
    if current_user.clinic_id != filled_form.patient.clinic_id:
        return jsonify(error='Вам запрещено совершать это действие'), 403
    db_sess.query(FilledForm).filter_by(id=filled_form_id).delete()
    db_sess.commit()
    return jsonify(success='OK'), 200


@blueprint.route('/api/filled_forms/', methods=['GET'])
@blueprint.route('/api/filled_forms', methods=['GET'])
@login_required
def get_filled_forms():
    verdict = assert_account_type(['Doctor', 'Admin'])
    if verdict is not None:
        return verdict
    db_sess = db_sessionmaker.create_session()
    clinic_patients = db_sess.query(Patient.id.label('id')).filter(
        Patient.clinic_id == current_user.clinic_id).subquery()
    filled_forms = db_sess.query(FilledForm).filter(
        FilledForm.patient_id == clinic_patients.c.id).all()
    filled_forms_and_authors = [None] * len(filled_forms)
    for i, filled_form in enumerate(filled_forms):
        author = filled_form.patient
        filled_formdict = filled_form.to_dict()
        del filled_formdict['patient_id']
        filled_formdict['author_login'] = author.login
        filled_formdict['author_initials'] = ' '.join([
            author.surname, author.name, author.patronymic])
        filled_forms_and_authors[i] = filled_formdict
    return jsonify(filled_forms=filled_forms_and_authors), 200


filled_form_request_parser = reqparse.RequestParser()
filled_form_request_parser.add_argument('form_id', required=True, type=int)


@blueprint.route('/api/filled_forms/', methods=['POST'])
@blueprint.route('/api/filled_forms', methods=['POST'])
@login_required
def create_filled_form():
    parser_request = req_manager.get_request('POST')
    verdict = assert_account_type('Patient')
    if verdict is not None:
        return verdict
    args = filled_form_request_parser.parse_args(req=parser_request)
    verdict = abort_if_model_not_found(Form, args['form_id'])
    if verdict is not None:
        return verdict
    db_sess = db_sessionmaker.create_session()
    form = db_sess.query(Form).get(args['form_id'])
    if form.clinic_id != current_user.clinic_id:
        return jsonify(error='Данная анкета не из Вашей поликлиники'), 403
    filled_form = FilledForm(form=form, patient_id=current_user.id)
    db_sess.add(filled_form)
    db_sess.commit()
    return jsonify(success='OK'), 200
