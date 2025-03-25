from django.utils.translation import gettext as _
from rest_framework.exceptions import NotFound, ParseError

from core.system.authentication.models import AuthUserAccessToken
from core.repositories import BaseRepository
from core.system.mfa.devices.email.services.otp_email_service import OTPEmailService
from core.system.mfa.devices.totp.services.otp_totp_service import OtpTotpService


class UserMFAService:
    repository = BaseRepository()

    def register_email_otp(self, user_uid, email):
        """
        Register email otp for user
        @param user_uid:
        @param email:
        @return:
        """
        admin = self._get_user_by_uid(user_uid)

        email_otp_service = OTPEmailService()
        return email_otp_service.register_email_otp_device(admin, email)

    def register_totp_otp(self, user_uid):
        """
        Register totp otp for user
        @param user_uid:
        @return:
        """
        admin = self._get_user_by_uid(user_uid)

        email_otp_service = OtpTotpService()
        return email_otp_service.register_totp_otp_device(admin)

    def get_user_totp_detail(self, user_uid):
        """
        Get user totp detail for user
        @param user_uid:
        @return:
        """
        admin = self._get_user_by_uid(user_uid)
        email_otp_service = OtpTotpService()
        totp_device = email_otp_service.get_totp_otp_device(admin)
        qrcode = email_otp_service.generate_qr_code(totp_device)

        return totp_device, qrcode

    def verify_mfa(self, user, access_token: AuthUserAccessToken, verify_code: str):
        """
        Verify FMA for login session
        @param user:
        @param access_token:
        @param verify_code:
        @return:
        """
        totp_device = user.get_otp_totp_device()
        email_device = user.get_otp_email_device()
        is_matched = False
        if totp_device is not None:
            is_matched = totp_device.verify_token(verify_code)
        if not is_matched and email_device:
            is_matched = email_device.verify_token(verify_code)

        if is_matched:
            access_token.is_mfa_verified = True
            access_token.save()

        return is_matched

    def resend_email_otp_code(self, user):
        """
        Resend Verify Email OTP code for login session
        @param user:
        @return:
        """
        email_device = user.get_otp_email_device()
        if email_device is None:
            raise ParseError(_('error_user_not_register_otp'))

        email_device.generate_challenge(send_mail=True)

    def _get_user_by_uid(self, user_uid):
        """
        Get user by uid
        @param user_uid:
        @return:
        """
        user = self.repository.find_by_uid(user_uid)

        if user is None:
            raise NotFound(_('error_user_not_found'))

        return user
