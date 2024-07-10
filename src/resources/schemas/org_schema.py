from copy import deepcopy

from src.resources.schemas.user_schema import user_all_fields
from src.resources.utils import map_rest_schema
from flask_restful import fields

org_all_attributes = {
    'name': {
        'type': str,
        'required': True,
    },
    'ABN': {
        'type': str,
        'required': True,
    },
    'contact_email': {
        'type': str,
        'required': True,
    },
    'contact_phone': {
        'type': str,
    },
    'billing_address': {
        'type': str,
    },
    'logo_url': {
        'type': str,
    }
}

org_return_attributes = {
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

org_all_fields = {}
map_rest_schema(org_return_attributes, org_all_fields)
map_rest_schema(org_all_attributes, org_all_fields)

org_all_fields_with_children_base = {
    'users': fields.List(fields.Nested(user_all_fields))
}
org_all_fields_with_children = deepcopy(org_all_fields)
org_all_fields_with_children.update(org_all_fields_with_children_base)
