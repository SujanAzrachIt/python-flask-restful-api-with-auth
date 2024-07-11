from abc import abstractmethod

from flask_restful import reqparse, marshal_with, abort

from src.http.exception.exception import NotFoundException
from src.middlewares.auth_middleware import auth_required
from src.models.org.model_org import OrgModel
from src.resources.org.org_base import OrgBase
from src.resources.schemas.org_schema import org_all_attributes, org_all_fields


class OrgSingular(OrgBase):
    patch_parser = reqparse.RequestParser()
    for attr in org_all_attributes:
        patch_parser.add_argument(attr,
                                  type=org_all_attributes[attr]['type'],
                                  required=False,
                                  store_missing=False)

    @classmethod
    @auth_required('org_admin')
    @marshal_with(org_all_fields)
    def get(cls, **kwargs):
        org = cls.get_org(**kwargs)
        if not org:
            raise NotFoundException('Organization not found')
        return org

    @classmethod
    def delete(cls, **kwargs):
        org = cls.get_org(**kwargs)
        if not org:
            raise NotFoundException('Organization not found')
        org.delete_from_db()
        return '', 204

    @classmethod
    @marshal_with(org_all_fields)
    def put(cls, **kwargs):
        data = cls.parser.parse_args()
        org: OrgModel = cls.get_org(**kwargs)
        if not org:
            return cls.add_org(data)
        return org.update(**data)

    @classmethod
    @marshal_with(org_all_fields)
    def patch(cls, **kwargs):
        data = cls.patch_parser.parse_args()
        org: OrgModel = cls.get_org(**kwargs)
        if not org:
            raise NotFoundException('Organization not found')
        return org.update(**data)

    @classmethod
    @abstractmethod
    def get_org(cls, **kwargs) -> OrgModel:
        return OrgModel.find_by_id(kwargs.get('id'))