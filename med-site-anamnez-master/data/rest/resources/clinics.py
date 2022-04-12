from flask import Blueprint, jsonify
from data.db.models.clinic import Clinic
from data.db import db_sessionmaker
from data.rest.rest_utils import abort_if_model_not_found


blueprint = Blueprint(
    'clinics_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/clinics/<int:clinic_id>/', methods=['GET'])
@blueprint.route('/api/clinics/<int:clinic_id>', methods=['GET'])
def get_one_clinic(clinic_id: int):
    verdict = abort_if_model_not_found(Clinic, clinic_id)
    if verdict is not None:
        return verdict
    db_sess = db_sessionmaker.create_session()
    clinic = db_sess.query(Clinic).get(clinic_id)
    return jsonify(clinic=clinic.to_dict()), 200


@blueprint.route('/api/clinics/', methods=['GET'])
@blueprint.route('/api/clinics', methods=['GET'])
def get_clinics():
    db_sess = db_sessionmaker.create_session()
    clinics = db_sess.query(Clinic).all()
    clinics = tuple(clinic.to_dict() for clinic in clinics)
    return jsonify(clinics=clinics), 200
