import os
from abc import abstractmethod

from flask import request
from flask_restful import reqparse, marshal_with

from src.enums.role import Role
from src.http.exception.exception import NotFoundException
from src.models.user.model_user import UserModel
from src.resources.schemas.user_schema import user_all_attributes, user_all_fields
from src.resources.user.user_base import UserBase


class UserSingular(UserBase):
    patch_parser = reqparse.RequestParser()
    for attr in user_all_attributes:
        patch_parser.add_argument(attr,
                                  type=user_all_attributes[attr]['type'],
                                  required=False,
                                  store_missing=False,
                                  location='json')

    @classmethod
    @marshal_with(user_all_fields)
    def get(cls, **kwargs):
        user = cls.get_user(**kwargs)
        if not user:
            raise NotFoundException('User not found')
        return user

    @classmethod
    def delete(cls, **kwargs):
        user = cls.get_user(**kwargs)
        if not user:
            raise NotFoundException('User not found')
        user.soft_delete()
        return '', 204

    @classmethod
    @marshal_with(user_all_fields)
    def put(cls, **kwargs):
        data = cls.parser.parse_args()
        roles = request.get_json()['roles']
        user: UserModel = cls.get_user(**kwargs)
        if not user:
            return cls.add_user(data, roles)
        return user.update(**data)

    @classmethod
    @marshal_with(user_all_fields)
    def patch(cls, **kwargs):
        data = cls.patch_parser.parse_args()
        user: UserModel = cls.get_user(**kwargs)
        if not user:
            raise NotFoundException('User not found')
        return user.update(**data)

    @classmethod
    @abstractmethod
    def get_user(cls, **kwargs) -> UserModel:
        return UserModel.find_by_id(kwargs.get('id'))


class SuperAdminUserSingular(UserBase):
    @classmethod
    @marshal_with(user_all_fields)
    def post(cls):
        super_admin_data = {
            "phone_number": os.getenv('SUPER_ADMIN_PHONE_NUMBER', '+10000000000'),
            "formatted_phone_number": os.getenv('SUPER_ADMIN_FORMATTED_PHONE_NUMBER', '+1 (000) 000-0000'),
            "email": os.getenv('SUPER_ADMIN_EMAIL', 'superadmin@example.com'),
            "password": os.getenv('SUPER_ADMIN_PASSWORD', 'SuperAdminPassword123'),
            "is_email_verified": True,
            "is_active": True
        }

        user: UserModel = cls.add_user(super_admin_data, [Role.SUPER_ADMIN.name])

        return user
