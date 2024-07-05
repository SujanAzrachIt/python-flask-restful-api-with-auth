from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

from src.models.model_base import ModelBase

db = SQLAlchemy()


class QrCodeModel(ModelBase):
    __tablename__ = 'qr_codes'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    location = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Numeric(10, 8), nullable=True)
    longitude = db.Column(db.Numeric(11, 8), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    org_id = db.Column(db.String(36), db.ForeignKey('orgs.id'), nullable=True)

    # TODO: add fields needed and improvement on column type and size
    def __repr__(self):
        return f"QrCode(id = {self.id})"

    @classmethod
    def find_by_id(cls, _id: str):
        return cls.query.filter_by(id=_id).first()

