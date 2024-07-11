from copy import deepcopy

from flask_restful import fields

from src.resources.schemas.role_schema import role_all_fields
from src.resources.utils import map_rest_schema

user_all_attributes = {
    'phone_number': {
        'type': str,
        'required': True,
    },
    'formatted_phone_number': {
        'type': str,
        'required': True,
    },
    'email': {
        'type': str,
        'required': True,
    },
    'password': {
        'type': str,
        'required': True,
    },
    'is_email_verified': {
        'type': bool,
    },
    'org_id': {
        'type': str,
    },
    'is_active': {
        'type': bool,
    },
}

user_return_attributes = {
    'id': {
        'type': str,
    },
    'created_on': {
        'type': str,
    },
    'updated_on': {
        'type': str,
    }
}

user_all_fields = {}
map_rest_schema(user_return_attributes, user_all_fields)
map_rest_schema(user_all_attributes, user_all_fields)

user_all_fields_with_children_base = {
    'roles': fields.List(fields.Nested(role_all_fields))
}
user_all_fields_with_children = deepcopy(user_all_fields)
user_all_fields_with_children.update(user_all_fields_with_children_base)