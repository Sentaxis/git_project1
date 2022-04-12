import os
from flask import Flask
from config import AppConfig
from data.db import db_sessionmaker
from data.rest import rest_api_manager
from data import auth, recover, errorhandling, interface


app = Flask(__name__)
app.config.from_object(AppConfig)


if __name__ == '__main__':
    DB_DIRNAME = 'database'
    DB_FILENAME = 'med_site_anamnez.sqlite'
    db_sessionmaker.global_init(
        os.path.join(DB_DIRNAME, DB_FILENAME))
    auth.register_login_manager(app)
    app.register_blueprint(auth.blueprint)
    rest_api_manager.global_api_init(app)
    app.register_blueprint(recover.blueprint)
    app.register_blueprint(interface.blueprint)
    errorhandling.register_errorhandlers(app)
    app.run(host='127.0.0.1', port=5000, debug=True)
