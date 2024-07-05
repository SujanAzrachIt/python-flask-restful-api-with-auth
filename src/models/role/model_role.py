from flask_sqlalchemy import SQLAlchemy
import uuid

from sqlalchemy import Enum

from src.enums.role import Role
from src.models.model_base import ModelBase
from src.models.user_role.model_user_role import UserRolesModel

db = SQLAlchemy()


class RoleModel(ModelBase):
    __tablename__ = 'roles'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(Enum(Role), unique=True, nullable=False)

    users = db.relationship('UserModel', secondary=UserRolesModel.__tablename__, back_populates='roles')

    @classmethod
    def find_by_id(cls, _id: str):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_by_roles(cls, roles: list):
        return cls.query.filter(cls.name.in_(roles)).all()