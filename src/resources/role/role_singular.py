from abc import abstractmethod

from flask_restful import reqparse, marshal_with

from src.http.exception.exception import NotFoundException
from src.models.role.model_role import RoleModel
from src.resources.role.role_base import RoleBase
from src.resources.schemas.role_schema import role_all_attributes, role_all_fields


class RoleSingular(RoleBase):
    patch_parser = reqparse.RequestParser()
    for attr in role_all_attributes:
        patch_parser.add_argument(attr,
                                  type=role_all_attributes[attr]['type'],
                                  required=False,
                                  store_missing=False)

    @classmethod
    @marshal_with(role_all_fields)
    def get(cls, **kwargs):
        org = cls.get_role(**kwargs)
        if not org:
            raise NotFoundException('Role not found')
        return org

    @classmethod
    def delete(cls, **kwargs):
        org = cls.get_role(**kwargs)
        if not org:
            raise NotFoundException('Role not found')
        org.delete_from_db()
        return '', 204

    @classmethod
    @marshal_with(role_all_fields)
    def put(cls, **kwargs):
        data = cls.parser.parse_args()
        role: RoleModel = cls.get_role(**kwargs)
        if not role:
            return cls.add_role(data)
        return role.update(**data)

    @classmethod
    @marshal_with(role_all_fields)
    def patch(cls, **kwargs):
        data = cls.patch_parser.parse_args()
        role: RoleModel = cls.get_role(**kwargs)
        if not role:
            raise NotFoundException('Role not found')
        return role.update(**data)

    @classmethod
    @abstractmethod
    def get_role(cls, **kwargs) -> RoleModel:
        return RoleModel.find_by_id(kwargs.get('id'))