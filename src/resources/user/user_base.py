from flask_restful import Resource, reqparse

from src.enums.role import Role
from src.models.role.model_role import RoleModel
from src.models.user.model_user import UserModel
from src.resources.schemas.user_schema import user_all_attributes


class UserBase(Resource):
    parser = reqparse.RequestParser()
    for attr in user_all_attributes:
        parser.add_argument(attr,
                            type=user_all_attributes[attr].get('type'),
                            required=user_all_attributes[attr].get('required', False),
                            help=user_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    def add_user(cls, data, roles):
        user = UserModel(**data)

        # encrypt password
        user.encrypt_password(user.password)

        # assign roles
        role_enum_values = [Role[name] for name in roles if name in Role.__members__]
        user.roles = RoleModel.get_by_roles(role_enum_values)

        user.save_to_db()
        return user