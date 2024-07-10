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
    'created_on': {
        'type': str,
    },
    'updated_on': {
        'type': str,
    }
}

role_all_fields = {}
map_rest_schema(role_return_attributes, role_all_fields)
map_rest_schema(role_all_attributes, role_all_fields)