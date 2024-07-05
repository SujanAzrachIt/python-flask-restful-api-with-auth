from abc import abstractmethod

from flask_restful import reqparse, Resource

from src.resources.schemas.auth_schema import auth_request_attribute


class AuthBase(Resource):
    parser = reqparse.RequestParser()
    for attr in auth_request_attribute:
        parser.add_argument(attr,
                            type=auth_request_attribute[attr]['type'],
                            required=auth_request_attribute[attr].get('required', False),
                            help=auth_request_attribute[attr].get('help', None),
                            store_missing=False)

    @classmethod
    def parse_args(cls):
        return cls.parser.parse_args()

    @abstractmethod
    def post(self):
        """To be implemented by subclasses."""
        pass
