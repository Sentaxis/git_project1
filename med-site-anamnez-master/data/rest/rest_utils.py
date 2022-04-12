from flask import session, jsonify
from data.db import db_sessionmaker
from data.db.__all_models import USER_MODELS


TRANSLATE = {
    'Clinic': 'Поликниника',
    'Admin': 'Администратор',
    'Doctor': 'Врач',
    'Patient': 'Пациент',
    'Form': 'Анкета',
    'FilledForm': 'Результат опроса'
}


def abort_if_model_not_found(model, model_id: int):
    db_sess = db_sessionmaker.create_session()
    if not db_sess.query(model).get(model_id):
        return jsonify(error=f'{TRANSLATE.get(model.__name__)} ' + (
            f'с номером={model_id} не найден(а)')), 404


def assert_account_type(account_types):
    if isinstance(account_types, str):
        account_types = [account_types]
    else:
        assert isinstance(account_types, list) and account_types
    if session['account_type'] not in map(str.capitalize, account_types):
        only_acc_type = TRANSLATE.get(account_types[0].capitalize()).lower()
        return jsonify(error=f'Только {only_acc_type} может это делать'), 403


def abort_if_user_exists(user_login: str):
    db_sess = db_sessionmaker.create_session()
    for model in USER_MODELS:
        if db_sess.query(model).filter_by(
                login=user_login).first() is not None:
            return jsonify(error=(
                'Пользователь с таким логином уже зарегистрирован')), 400


def get_required_strs_args_names(parser_args):
    return [
        arg.name for arg in parser_args
        if arg.type is str and arg.required]


def abort_if_blank_str_in_args(args, str_fields_names):
    for str_field_name in str_fields_names:
        str_field_name: str  # гарантируется, что is_required=True
        if not args[str_field_name]:
            return jsonify(
                error=f'Поле {str_field_name} оставлено пустым'), 400


def strip_strs_in_args(args, str_fields_names):
    for str_field_name in str_fields_names:
        str_field_name: str  # гарантируется, что is_required=True
        args[str_field_name] = args[str_field_name].strip()
