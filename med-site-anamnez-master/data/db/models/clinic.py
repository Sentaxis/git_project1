import sqlalchemy as sa
from sqlalchemy import orm
from data.db.db_sessionmaker import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Clinic(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'clinic'

    serialize_only = ('id', 'title', 'address')

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.Text, unique=False, nullable=False)
    address = sa.Column(sa.Text, unique=True, nullable=False)
    admins = orm.relationship(
        'Admin', backref=orm.backref('clinic', lazy=True))
    doctors = orm.relationship(
        'Doctor', backref=orm.backref('clinic', lazy=True))
    patients = orm.relationship(
        'Patient', backref=orm.backref('clinic', lazy=True))
    forms = orm.relationship(
        'Form', backref=orm.backref('clinic', lazy=True))

    def __repr__(self):
        return (f"Clinic(id={self.id}, "
                f"title='{self.title}', "
                f"address='{self.address}')")

    def __str__(self):
        return (f"Clinic(id={self.id}, "
                f"title='{self.title}', "
                f"address='{self.address}')")
