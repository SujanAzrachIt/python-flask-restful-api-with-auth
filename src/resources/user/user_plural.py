from abc import abstractmethod

from flask_restful.reqparse import request

from src.http.exception.exception import NotFoundException
from src.models.user.model_user import UserModel
from src.resources.user.user_base import UserBase, user_marshaller


class UserPlural(UserBase):
    @classmethod
    def get(cls, **kwargs):
        users: UserModel = cls.get_users(**kwargs)
        if not users:
            raise NotFoundException("Users not found")
        return user_marshaller(users, request.args)

    @classmethod
    @abstractmethod
    def get_users(cls, **kwargs):
        return UserModel.find_all()


class UserPluralByOrgId(UserPlural):
    @classmethod
    def get_users(cls, **kwargs):
        return UserModel.find_by_org_id(kwargs.get('org_id'))
