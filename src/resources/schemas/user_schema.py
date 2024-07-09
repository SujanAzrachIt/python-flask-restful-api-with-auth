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
    'preferred_phone_number': {
        'type': str,
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
    'created_at': {
        'type': str,
    },
    'updated_at': {
        'type': str,
    }
}

user_all_fields = {}
map_rest_schema(user_return_attributes, user_all_fields)
map_rest_schema(user_all_attributes, user_all_fields)
