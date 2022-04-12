import sqlalchemy as sa
from sqlalchemy import orm
from data.db.db_sessionmaker import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Form(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'form'

    serialize_only = (
        'id', 'title', 'clinic_id')

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.Text, unique=False, nullable=False)
    clinic_id = sa.Column(
        sa.Integer, sa.ForeignKey('clinic.id'), nullable=False)
    filled_forms = orm.relationship(
        'FilledForm', backref=orm.backref('form', lazy=True))

    def __repr__(self):
        return (f"Form(id={self.id}, "
                f"title={self.title!r}, "
                f"clinic_id={self.clinic_id!r})")

    def __str__(self):
        return (f"<Form id={self.id}, "
                f"title={self.title!r}, "
                f"clinic_id={self.clinic_id!r}>")
