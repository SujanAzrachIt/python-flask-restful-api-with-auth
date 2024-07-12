import datetime
import os

import jwt

from src.http.exception.exception import BadDataException, ForbiddenException
from src.models.user.model_user import UserModel
from src.services.auth.models.auth_model import MagicLinkResponseDTO, SignInResponseDTO, SignInRequestDTO
from src.services.sms.sms_service import SmsService
from src.utils.singleton import Singleton


class AuthService(metaclass=Singleton):
    def __init__(self):
        self.jwt_secret = os.getenv('JWT_SECRET', 'secret')

    def _generate_token(self, payload):
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')

    def generate_magic_link(self, user: UserModel, entry_point: str):
        roles = user.get_role_names()

        if 'super_admin' in roles or 'admin' in roles or 'org_admin' in roles:
            response = MagicLinkResponseDTO(
                message='Admin Credentials Required',
                admin_sign_in_required=True
            )
            return response.__dict__

        magic_link_token_payload = {
            "user_id": user.id,
            "role": roles,
            "orgId": user.org_id,
            "magic_link_entry_point": entry_point,
            "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=3600)
        }
        magic_link_token = self._generate_token(magic_link_token_payload)

        base_url = os.getenv('BASE_URL', 'http://localhost:3000')
        magic_link = f"{base_url}/?token={magic_link_token}"

        sms_message_body = f"Your login link is {magic_link}"
        SmsService().send_magic_link_sms(user.formatted_phone_number, sms_message_body)

        response = MagicLinkResponseDTO(
            message='Magic link generated',
            magic_link=magic_link
        )

        return response.__dict__

    def sign_in(self, dto: SignInRequestDTO, user: UserModel):
        if not user.is_active:
            raise ForbiddenException("Account is inactive")

        roles = user.get_role_names()

        if 'super_admin' in roles or 'admin' in roles or 'org_admin' in roles:
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

            response = SignInResponseDTO(
                message='Admin authenticated successfully',
                token=admin_token,
                role=roles,
                user_id=user.id,
                org_id=user.org_id,
                redirect_url=dto.entry_point
            )
            return response.__dict__

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

        response = SignInResponseDTO(
            message='Sign-in successful',
            token=sign_in_token,
            role=roles,
            user_id=user.id,
            org_id=user.org_id,
            redirect_url=dto.entry_point
        )
        return response.__dict__

    def request_otp(self, user: UserModel):
        if not user.is_active:
            raise ForbiddenException("Account is inactive")

        SmsService().send_sms(user.formatted_phone_number)

        return {'message': 'OTP sent successfully'}
