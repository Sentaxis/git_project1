from data.rest.resources import clinics
from data.rest.resources import doctors
from data.rest.resources import patients
from data.rest.resources import filled_forms


def global_api_init(app):
    app.register_blueprint(clinics.blueprint)
    app.register_blueprint(doctors.blueprint)
    app.register_blueprint(patients.blueprint)
    app.register_blueprint(filled_forms.blueprint)
