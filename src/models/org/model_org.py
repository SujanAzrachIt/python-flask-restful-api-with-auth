import uuid

from flask_sqlalchemy import SQLAlchemy

from src.models.model_base import ModelBase

db = SQLAlchemy()


class OrgModel(ModelBase):
    __tablename__ = 'orgs'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String, nullable=False, unique=True)
    ABN = db.Column(db.String, nullable=False, unique=True)
    contact_email = db.Column(db.String, nullable=False)
    contact_phone = db.Column(db.String)
    billing_address = db.Column(db.String)
    logo_url = db.Column(db.String(1024), nullable=True)

    # Define any model associations here, if necessary
    users = db.relationship('UserModel', backref='orgs', lazy=True)
    qr_codes = db.relationship('QrCodeModel', backref='orgs', lazy=True)

    # TODO: add fields needed and improvement on column type and size
    def __repr__(self):
        return f"Org(uuid = {self.id})"

    @classmethod
    def find_by_id(cls, _id: str):
        return cls.query.filter_by(id=_id).first()
