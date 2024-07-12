from flask_restful import reqparse

from src.http.exception.exception import NotFoundException
from src.models.user.model_user import UserModel
from src.resources.auth.auth_base import AuthBase
from src.resources.schemas.auth_schema import magic_link_generate_attribute, sign_in_attribute
from src.services.auth.auth_service import AuthService
from src.services.auth.models.auth_model import SignInRequestDTO


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

        user = UserModel.find_by_phone_number(data['phone_number'])
        if not user:
            raise NotFoundException('User not found')

        result = AuthService().generate_magic_link(user, data.get('magic_link_entry_point', '/'))
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

        user = UserModel.find_by_phone_number(data['phone_number'])
        if not user:
            raise NotFoundException('User not found')

        result = AuthService().sign_in(dto, user)
        return result


class RequestOTPSingular(AuthBase):

    @classmethod
    def post(cls):
        data = cls.parse_args()

        user = UserModel.find_by_phone_number(data['phone_number'])
        if not user:
            raise NotFoundException('User not found')

        result = AuthService().request_otp(user)
        return result
