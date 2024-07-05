import base64
import io
import urllib

import qrcode

from src.utils.singleton import Singleton


class QrCodeService(metaclass=Singleton):
    def __init__(self, base_url):
        self.base_url = base_url

    def generate_qr_code(self, qr_code_data):
        # Construct the dynamic URL to embed in the QR code
        location_encoded = urllib.parse.quote(qr_code_data.location)
        url_to_embed = f'{self.base_url}/confirm-service?status=Confirmed&qrCodeId={qr_code_data.id}&location={location_encoded}'

        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(url_to_embed)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        # Convert image to base64
        buffer = io.BytesIO()
        img.save(buffer, 'PNG')
        qr_code_image = buffer.getvalue()
        qr_code_image_base64 = base64.b64encode(qr_code_image).decode('utf-8')

        response = {
            'qrCodeImage': f'data:image/png;base64,{qr_code_image_base64}',
            'urlToEmbed': url_to_embed
        }

        return response