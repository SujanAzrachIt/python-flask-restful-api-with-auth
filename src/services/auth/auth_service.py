import datetime
import os
import random

import jwt
from sqlalchemy.exc import SQLAlchemyError

from src.dtos.request.magic_link_request_dto import MagicLinkRequestDTO
from src.dtos.request.sign_in_request_dto import SignInRequestDTO
from src.dtos.response.sign_in_response_dto import SignInResponseDTO
from src.models.user.model_user import UserModel
from src.utils.singleton import Singleton


class AuthService(metaclass=Singleton):
    def __init__(self):
        self.jwt_secret = os.getenv('JWT_SECRET', 'secret')

    def _generate_token(self, payload):
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')

    @staticmethod
    def _get_user_by_phone(phone_number) -> UserModel:
        user = UserModel.find_by_phoneNumber(phone_number)
        if not user:
            raise ValueError('User not found')
        return user

    def generate_magic_link(self, dto: MagicLinkRequestDTO):
        if not dto.phone_number:
            return {'message': 'Mobile Phone Number is required'}, 400

        try:
            user = self._get_user_by_phone(dto.phone_number)

            if 'orgAdmin' in user.roles:
                return {'adminSignInRequired': True}, 200

            entry_point = dto.magic_link_entry_point
            roles = user.get_role_names()

            magic_link_token_payload = {
                "userId": user.id,
                "role": roles,
                "orgId": user.org_id,
                "preferredPhoneNumber": user.preferred_phone_number,
                "magicLinkEntryPoint": entry_point,
            }
            magic_link_token = self._generate_token(magic_link_token_payload)

            sign_in_token_payload = {
                'userId': user.id,
                'role': roles,
                'orgId': user.org_id,
                'entryPoint': entry_point
            }
            sign_in_token = self._generate_token(sign_in_token_payload)

            base_url = os.getenv('BASE_URL', 'http://localhost:1610')
            magic_link = f"{base_url}/?token={magic_link_token}"

            return {
                'message': 'Magic link generated',
                'magicLink': magic_link,
                'signInToken': sign_in_token
            }, 200

        except ValueError as e:
            return {'message': str(e)}, 404
        except SQLAlchemyError as e:
            return {'message': 'An error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An error occurred', 'error': str(e)}, 500

    def sign_in(self, dto: SignInRequestDTO):
        if not dto.phone_number:
            return {'message': 'Mobile Phone Number is required'}, 400

        try:
            user = self._get_user_by_phone(dto.phone_number)
            if not user:
                return {'message': 'User not found'}, 404

            if not user.is_active:
                return {'message': 'Account is inactive'}, 403

            roles = user.get_role_names()
            if 'orgAdmin' in roles:
                if not dto.email or not dto.password:
                    return {'message': 'Email and password are required for admin sign-in'}, 400

                if user.email != dto.email:
                    return {'message': 'Invalid email or password'}, 401

                if not user.check_password(dto.password):
                    return {'message': 'Invalid email or password'}, 401

                if not user.is_email_verified:
                    return {'message': 'Admin email is not verified. Please verify to continue.'}, 304

                payload = {
                    'userId': user.id,
                    'role': roles,
                    'orgId': user.org_id,
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

            if not dto.bypass_otp:
                if not dto.otp:
                    return {'message': 'OTP is required for non-admin sign-in'}, 400

                if user.otp != dto.otp or user.otp_expire < datetime.datetime.now(datetime.UTC):
                    return {'message': 'Invalid or expired OTP'}, 401

            sign_in_token_payload = {
                'userId': user.id,
                'role': roles,
                'orgId': user.org_id,
                'entryPoint': dto.entry_point,
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

        except SQLAlchemyError as e:
            return {'message': 'An error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An error occurred', 'error': str(e)}, 500

    def request_otp(self, phone_number: str):
        if not phone_number:
            return {'message': 'Mobile Phone Number is required'}, 400

        try:
            user = self._get_user_by_phone(phone_number)

            if not user.is_active:
                return {'message': 'Account is inactive'}, 403

            if user.otp_expire and user.otp_expire > datetime.datetime.now(datetime.UTC):
                return {'message': 'OTP already requested and not expired'}, 400

            otp_value = random.randint(100000, 999999)
            otp_expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=5)

            user.otp = otp_value
            user.otp_expire = otp_expire
            user.update()
            # self._send_otp(phone_number, otp_value)

            return {'message': 'OTP sent successfully'}, 200

        except ValueError as e:
            return {'message': str(e)}, 404
        except SQLAlchemyError as e:
            return {'message': 'An error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An error occurred', 'error': str(e)}, 500
