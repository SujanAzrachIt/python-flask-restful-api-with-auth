import logging
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

    def send_magic_link_sms(self, phone_number, message_body):
        try:
            message = self.client.messages.create(
                body=message_body,
                from_="+9779860171119",
                to="+9779861308907",
            )
        except TwilioRestException as e:
            logging.error(f"Failed to send magic link SMS to {phone_number}: {e}")
            return None

        return message.status

    def send_sms(self, phone_number):
        try:
            verification = self.client.verify.v2.services(self.twilio_service_sid).verifications.create(
                channel="sms",
                to=phone_number
            )
            return verification.status
        except TwilioRestException as e:
            logging.error(f"Failed to send verification code SMS to {phone_number}: {e}")
            return None

    def verify_totp_code(self, phone_number, code):
        try:
            verification_check = self.client.verify.v2.services(self.twilio_service_sid).verification_checks.create(
                to=phone_number,
                code=code
            )
            return verification_check.status == 'approved'
        except TwilioRestException as e:
            logging.error(f"Failed to verify TOTP code for {phone_number}: {e}")
            return False
