from flask_restful import reqparse

from src.dtos.request.magic_link_request_dto import MagicLinkRequestDTO
from src.dtos.request.sign_in_request_dto import SignInRequestDTO
from src.resources.auth.auth_base import AuthBase
from src.resources.schemas.auth_schema import magic_link_generate_attribute, sign_in_attribute
from src.services.auth.auth_service import AuthService


class GenerateMagicLinkSingular(AuthBase):
    patch_parser = reqparse.RequestParser()
    for attr in magic_link_generate_attribute:
        patch_parser.add_argument(attr,
                                  type=magic_link_generate_attribute[attr]['type'],
                                  required=False,
                                  store_missing=False)

    @classmethod
    def post(cls):
        data = cls.patch_parser.parse_args()
        dto = MagicLinkRequestDTO(
            phone_number=data['phone_number'],
            magic_link_entry_point=data.get('magic_link_entry_point', '/')
        )

        result = AuthService().generate_magic_link(dto)
        return result


class SignInSingular(AuthBase):
    patch_parser = reqparse.RequestParser()
    for attr in sign_in_attribute:
        patch_parser.add_argument(attr,
                                  type=sign_in_attribute[attr]['type'],
                                  required=sign_in_attribute[attr].get('required', False),
                                  help=sign_in_attribute[attr].get('help', None),
                                  store_missing=False)

    @classmethod
    def post(cls):
        data = cls.patch_parser.parse_args()
        dto = SignInRequestDTO(
            phone_number=data.get('phone_number'),
            otp=data.get('otp'),
            entry_point=data.get('entry_point', '/'),
            bypass_otp=data.get('bypass_otp', False),
            email=data.get('email'),
            password=data.get('password')
        )

        result = AuthService().sign_in(dto)
        return result


class RequestOTPSingular(AuthBase):

    @classmethod
    def post(cls):
        data = cls.parse_args()
        result = AuthService().request_otp(data.get('phone_number'))
        return result
