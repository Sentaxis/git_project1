from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField
from wtforms.fields import EmailField, StringField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField('Логин:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня:')
    submit = SubmitField('Вход')


class RegisterForm(FlaskForm):
    login = StringField('Логин:', validators=[DataRequired()])
    name = StringField('Имя:', validators=[DataRequired()])
    surname = StringField('Фамилия:', validators=[DataRequired()])
    patronymic = StringField('Отчество:', validators=[DataRequired()])
    email = EmailField('Почта:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class RegisterDoctorForm(FlaskForm):
    login = StringField('Логин:', validators=[DataRequired()])
    name = StringField('Имя:', validators=[DataRequired()])
    surname = StringField('Фамилия:', validators=[DataRequired()])
    patronymic = StringField('Отчество:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    submit = SubmitField('Зарегистрировать')


class RegisterModeratorForm(FlaskForm):
    login = StringField('Логин:', validators=[DataRequired()])
    name = StringField('Имя:', validators=[DataRequired()])
    surname = StringField('Фамилия:', validators=[DataRequired()])
    patronymic = StringField('Отчество:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    submit = SubmitField('Зарегистрировать')


class RegisterClinicForm(FlaskForm):
    admin_login = StringField('Логин:', validators=[DataRequired()])
    admin_password = PasswordField('Пароль:', validators=[DataRequired()])
    name = StringField('Имя:', validators=[DataRequired()])
    surname = StringField('Фамилия:', validators=[DataRequired()])
    patronymic = StringField('Отчество:', validators=[DataRequired()])
    clinic_name = StringField('Название поликлиники:', validators=[DataRequired()])
    clinic_address = StringField('Адрес поликлиники:', validators=[DataRequired()])
    submit = SubmitField('Зарегистрировать')
