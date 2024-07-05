from flask_restful import Resource, reqparse

from src.models.org.model_org import OrgModel
from src.resources.schemas.org_schema import org_all_attributes


class OrgBase(Resource):
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