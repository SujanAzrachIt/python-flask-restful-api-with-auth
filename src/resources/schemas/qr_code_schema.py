from src.resources.utils import map_rest_schema

qrcode_all_attributes = {
    'location': {
        'type': str,
        'required': True,
    },
    'latitude': {
        'type': float,
    },
    'longitude': {
        'type': float,
    },
    'org_id': {
        'type': str,
    }
}

qrcode_return_attributes = {
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

qrcode_all_fields = {}
map_rest_schema(qrcode_return_attributes, qrcode_all_fields)
map_rest_schema(qrcode_all_attributes, qrcode_all_fields)