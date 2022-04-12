import sqlalchemy as sa
from data.db.db_sessionmaker import SqlAlchemyBase
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Patient(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'patient'

    serialize_only = (
        'id', 'login', 'surname',
        'name', 'patronymic', 'clinic_id')

    id = sa.Column(sa.Integer, primary_key=True)
    # является адресом электронной почты
    login = sa.Column(sa.Text, unique=True, nullable=False)
    passwd_hash = sa.Column(sa.Text, unique=False, nullable=False)
    surname = sa.Column(sa.Text, unique=False, nullable=False)
    name = sa.Column(sa.Text, unique=False, nullable=False)
    # отчество
    patronymic = sa.Column(sa.Text, unique=False, nullable=False)
    clinic_id = sa.Column(
        sa.Integer, sa.ForeignKey('clinic.id'), nullable=False)
    filled_forms = orm.relationship(
        'FilledForm', backref=orm.backref('patient', lazy=True))

    def set_password(self, new_password: str):
        self.passwd_hash = generate_password_hash(new_password)

    def check_password(self, password):
        return check_password_hash(self.passwd_hash, password)

    def __repr__(self):
        return (f"Patient(id={self.id}, "
                f"login='{self.login}', "
                f"passwd_hash='{self.passwd_hash}', "
                f"surname='{self.surname}', "
                f"name='{self.name}', "
                f"patronymic='{self.patronymic}', "
                f"clinic_id={self.clinic_id})")

    def __str__(self):
        return (f"<Patient id={self.id}, "
                f"login='{self.login}', "
                f"surname='{self.surname}', "
                f"name='{self.name}', "
                f"patronymic='{self.patronymic}', "
                f"clinic_id={self.clinic_id}>")
