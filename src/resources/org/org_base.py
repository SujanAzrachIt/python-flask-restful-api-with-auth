from flask_restful import reqparse

from src.http.resource import HttpResource
from src.models.org.model_org import OrgModel
from src.resources.schemas.org_schema import org_all_attributes, org_all_fields, org_all_fields_with_children
from src.resources.utils import model_marshaller_with_children


def org_marshaller(data: any, args: dict):
    return model_marshaller_with_children(data, args, org_all_fields,
                                          org_all_fields_with_children)


class OrgBase(HttpResource):
    parser = reqparse.RequestParser()
    for attr in org_all_attributes:
        parser.add_argument(attr,
                            type=org_all_attributes[attr].get('type'),
                            required=org_all_attributes[attr].get('required', False),
                            help=org_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    def add_org(cls, data):
        org = OrgModel(**data)
        org.save_to_db()

        return org
