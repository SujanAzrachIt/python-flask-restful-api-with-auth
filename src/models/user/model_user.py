import uuid

import bcrypt
from flask_sqlalchemy import SQLAlchemy

from src.models.model_base import ModelBase
from src.models.user_role.model_user_role import UserRolesModel

db = SQLAlchemy()


class UserModel(ModelBase):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    phone_number = db.Column(db.String, nullable=False, unique=True)
    formatted_phone_number = db.Column(db.String, nullable=False, unique=True)
    preferred_phone_number = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_email_verified = db.Column(db.Boolean, default=False)
    org_id = db.Column(db.String(36), db.ForeignKey('orgs.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    # # Define any model associations here, if necessary
    roles = db.relationship('RoleModel', secondary=UserRolesModel.__tablename__, back_populates='users')

    def __repr__(self):
        return f"User(uuid = {self.id})"

    @classmethod
    def find_by_id(cls, _id: str):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_phone_number(cls, _phone_number):
        return cls.query.filter_by(phone_number=_phone_number).first()

    def get_role_names(self):
        return [role.name.value for role in self.roles]

    def encrypt_password(self, password: str):
        """Hash the password and store it."""
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password = hashed_password.decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Check the provided password against the stored hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
