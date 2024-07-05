from flask_restful import Resource, reqparse

from src.models.role.model_role import RoleModel
from src.resources.schemas.role_schema import role_all_attributes


class RoleBase(Resource):
    parser = reqparse.RequestParser()
    for attr in role_all_attributes:
        parser.add_argument(attr,
                            type=role_all_attributes[attr].get('type'),
                            required=role_all_attributes[attr].get('required', False),
                            help=role_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    def add_role(cls, data):
        role = RoleModel(**data)
        role.save_to_db()
        return role