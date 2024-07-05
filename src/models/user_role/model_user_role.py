from flask_sqlalchemy import SQLAlchemy
import uuid

from src.models.model_base import ModelBase

db = SQLAlchemy()


class UserRolesModel(ModelBase):
    __tablename__ = 'user_roles'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    role_id = db.Column(db.String(36), db.ForeignKey('roles.id'), nullable=True)