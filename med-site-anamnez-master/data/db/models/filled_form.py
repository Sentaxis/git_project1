import datetime
import sqlalchemy as sa
from data.db.db_sessionmaker import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class FilledForm(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'filled_form'

    serialize_only = (
        'id', 'fill_datetime',
        'form_id', 'patient_id')

    id = sa.Column(sa.Integer, primary_key=True)
    fill_datetime = sa.Column(
        sa.DateTime, nullable=False, default=datetime.datetime.utcnow)
    form_id = sa.Column(
        sa.Integer, sa.ForeignKey('form.id'), nullable=False)
    patient_id = sa.Column(
        sa.Integer, sa.ForeignKey('patient.id'), nullable=False)

    def __repr__(self):
        return (f"FilledForm(id={self.id}, "
                f"fill_datetime={self.fill_datetime!r}, "
                f"form_id={self.form_id}, "
                f"patient_id={self.patient_id})")

    def __str__(self):
        return (f"<FilledForm id={self.id}, "
                f"fill_datetime={self.fill_datetime!r}, "
                f"form_id={self.form_id}, "
                f"patient_id={self.patient_id}>")
