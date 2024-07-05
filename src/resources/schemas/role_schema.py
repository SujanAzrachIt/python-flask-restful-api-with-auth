from src.resources.utils import map_rest_schema

role_all_attributes = {
    'name': {
        'type': str,
        'required': True,
    },
}

role_return_attributes = {
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

role_all_fields = {}
map_rest_schema(role_return_attributes, role_all_fields)
map_rest_schema(role_all_attributes, role_all_fields)