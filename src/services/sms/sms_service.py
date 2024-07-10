import os

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from src.utils.singleton import Singleton


class SmsService(metaclass=Singleton):
    def __init__(self):
        self.twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID', '')
        self.twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN', '')
        self.twilio_service_sid = os.getenv('TWILIO_SERVICE_SID', '')
        self.client = Client(self.twilio_account_sid, self.twilio_auth_token)

    def send_sms(self, phone_number):
        verification = self.client.verify.v2.services(self.twilio_service_sid).verifications.create(
            channel="sms",
            to=phone_number
        )
        return verification.status

    def verify_totp_code(self, phone_number, code):
        verification_check = self.client.verify.v2.services(
            "VAbb0a6ce6a831f2c480959ee4393f9401"
        ).verification_checks.create(to=phone_number, code=code)

        return verification_check.status == 'approved'
