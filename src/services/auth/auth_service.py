import datetime
import os

import jwt

from src.dtos.request.magic_link_request_dto import MagicLinkRequestDTO
from src.dtos.request.sign_in_request_dto import SignInRequestDTO
from src.dtos.response.sign_in_response_dto import SignInResponseDTO
from src.http.exception.exception import BadDataException, ForbiddenException, NotFoundException
from src.models.user.model_user import UserModel
from src.services.sms.sms_service import SmsService
from src.utils.singleton import Singleton


class AuthService(metaclass=Singleton):
    def __init__(self):
        self.jwt_secret = os.getenv('JWT_SECRET', 'secret')

    def _generate_token(self, payload):
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')

    @staticmethod
    def _get_user_by_phone(phone_number) -> UserModel:
        user = UserModel.find_by_phone_number(phone_number)
        if not user:
            raise NotFoundException('User not found')
        return user

    def generate_magic_link(self, dto: MagicLinkRequestDTO):
        if not dto.phone_number:
            raise BadDataException("Phone Number is required")

        user = self._get_user_by_phone(dto.phone_number)

        if 'org_admin' in user.roles:
            return {'admin_sign_in_required': True}, 200

        entry_point = dto.magic_link_entry_point
        roles = user.get_role_names()

        magic_link_token_payload = {
            "user_id": user.id,
            "role": roles,
            "orgId": user.org_id,
            "preferred_phone_number": user.preferred_phone_number,
            "magic_link_entry_point": entry_point,
        }
        magic_link_token = self._generate_token(magic_link_token_payload)

        sign_in_token_payload = {
            'user_id': user.id,
            'role': roles,
            'org_id': user.org_id,
            'entry_point': entry_point
        }

        sign_in_token = self._generate_token(sign_in_token_payload)
        base_url = os.getenv('BASE_URL', 'http://localhost:1610')
        magic_link = f"{base_url}/?token={magic_link_token}"

        return {
            'message': 'Magic link generated',
            'magic_link': magic_link,
            'sign_in_token': sign_in_token
        }, 200

    def sign_in(self, dto: SignInRequestDTO):
        if not dto.phone_number:
            raise BadDataException("Phone Number is required")

        user = self._get_user_by_phone(dto.phone_number)

        if not user.is_active:
            raise ForbiddenException("Account is inactive")

        roles = user.get_role_names()

        if 'org_admin' in roles:
            if not dto.email or not dto.password:
                raise BadDataException("Email and password are required for admin sign-in")

            if user.email != dto.email or not user.check_password(dto.password):
                raise BadDataException("Invalid email or password")

            if not user.is_email_verified:
                raise ForbiddenException("Admin email is not verified. Please verify to continue")

            payload = {
                'user_id': user.id,
                'role': roles,
                'org_id': user.org_id,
                "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=8600)
            }
            admin_token = self._generate_token(payload)

            response_dto = SignInResponseDTO(
                message='Admin authenticated successfully',
                token=admin_token,
                role=roles,
                user_id=user.id,
                org_id=user.org_id,
                redirect_url=dto.entry_point
            )
            return response_dto.__dict__, 200

        if not dto.otp:
            raise BadDataException("OTP is required for non-admin sign-in")

        verification_status = SmsService().verify_totp_code(user.formatted_phone_number, dto.otp)

        if not verification_status:
            raise ForbiddenException("Invalid OTP")

        sign_in_token_payload = {
            'user_id': user.id,
            'role': roles,
            'org_id': user.org_id,
            'entry_point': dto.entry_point,
            "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=3600)
        }
        sign_in_token = self._generate_token(sign_in_token_payload)

        response_dto = SignInResponseDTO(
            message='Sign-in successful',
            token=sign_in_token,
            role=roles,
            user_id=user.id,
            org_id=user.org_id,
            redirect_url=dto.entry_point
        )
        return response_dto.__dict__, 200

    def request_otp(self, phone_number: str):
        if not phone_number:
            raise NotFoundException("Phone Number is required")

        user = self._get_user_by_phone(phone_number)

        if not user.is_active:
            raise ForbiddenException("Account is inactive")

        SmsService().send_sms(user.formatted_phone_number)

        return {'message': 'OTP sent successfully'}, 200
