from werkzeug.exceptions import default_exceptions
from flask import jsonify


def versatile_errorhandler(error):
    try:
        error_data = error.data
    except AttributeError:
        error_data = {
            'error': f'[{error.code}] {error.name}. {error.description}'}
    return jsonify(**error_data), error.code


def register_errorhandlers(app):
    for status_code, http_exc in default_exceptions.items():
        if status_code < 400:
            continue
        app.register_error_handler(http_exc, versatile_errorhandler)
