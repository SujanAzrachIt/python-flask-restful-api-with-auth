from abc import abstractmethod

from flask_restful import reqparse, marshal_with

from src.http.exception.exception import NotFoundException
from src.models.qr_code.model_qr_code import QrCodeModel
from src.resources.qr_code.qr_code_base import QrCodeBase
from src.resources.schemas.qr_code_schema import qrcode_all_attributes, qrcode_all_fields
from src.services.qr_code.qr_code import QrCodeService


class QrCodeSingular(QrCodeBase):
    patch_parser = reqparse.RequestParser()
    for attr in qrcode_all_attributes:
        patch_parser.add_argument(attr,
                                  type=qrcode_all_attributes[attr]['type'],
                                  required=False,
                                  store_missing=False)

    @classmethod
    @marshal_with(qrcode_all_fields)
    def get(cls, **kwargs):
        qrCode: QrCodeModel = cls.get_qr_code(**kwargs)
        if not qrCode:
            raise NotFoundException('QrCode not found')
        return qrCode

    @classmethod
    def delete(cls, **kwargs):
        scraper: QrCodeModel = cls.get_qr_code(**kwargs)
        if not scraper:
            raise NotFoundException('QrCode not found')
        scraper.delete_from_db()
        return '', 204

    @classmethod
    @marshal_with(qrcode_all_fields)
    def put(cls, **kwargs):
        data = cls.parser.parse_args()
        qr_code: QrCodeModel = cls.get_qr_code(**kwargs)
        if not qr_code:
            return cls.add_qr_code(data)
        return qr_code.update(**data)

    @classmethod
    @marshal_with(qrcode_all_fields)
    def patch(cls, **kwargs):
        data = cls.patch_parser.parse_args()
        qr_code: QrCodeModel = cls.get_qr_code(**kwargs)
        if not qr_code:
            raise NotFoundException('QrCode not found')
        return qr_code.update(**data)

    @classmethod
    @abstractmethod
    def get_qr_code(cls, **kwargs) -> QrCodeModel:
        return QrCodeModel.find_by_id(kwargs.get('id'))


class GenerateQrCodeSingular(QrCodeBase):
    @classmethod
    def get(cls, **kwargs):
        qr_code: QrCodeModel = QrCodeModel.find_by_id(kwargs.get('id'))
        if not qr_code:
            raise NotFoundException('QR code not found')

        qr_code_service = QrCodeService(base_url='http://localhost:3000')
        response = qr_code_service.generate_qr_code(qr_code_data=qr_code)

        return response, 200
