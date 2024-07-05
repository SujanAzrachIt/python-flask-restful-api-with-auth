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
    'created_at': {
        'type': str,
    },
    'updated_at': {
        'type': str,
    }
}

org_all_fields = {}
map_rest_schema(org_return_attributes, org_all_fields)
map_rest_schema(org_all_attributes, org_all_fields)