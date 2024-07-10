from flask_restful import reqparse

from src.http.resource import HttpResource
from src.models.qr_code.model_qr_code import QrCodeModel
from src.resources.schemas.qr_code_schema import qrcode_all_attributes


class QrCodeBase(HttpResource):
    parser = reqparse.RequestParser()
    for attr in qrcode_all_attributes:
        parser.add_argument(attr,
                            type=qrcode_all_attributes[attr].get('type'),
                            required=qrcode_all_attributes[attr].get('required', False),
                            help=qrcode_all_attributes[attr].get('help', None),
                            store_missing=False)

    @classmethod
    def add_qr_code(cls, data):
        qr_code = QrCodeModel(**data)
        qr_code.save_to_db()
        return qr_code
