import base64

from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AuthUserResetPasswordTokenGenerator(PasswordResetTokenGenerator):

    def make_token(self, user):
        """
        Make reset password token for user
        @param user:
        @return:
        """
        token = super().make_token(user)
        email = getattr(user, 'email', '') or ''
        return self._make_user_friendly_token(email, token)

    def _make_hash_value(self, user, timestamp):
        """
        Make hash value for reset password token
        @param user:
        @param timestamp:
        @return:
        """
        login_timestamp = (
            ""
            if user.last_login is None
            else user.last_login.replace(microsecond=0, tzinfo=None)
        )
        email_field = user.get_email_field_name()
        email = getattr(user, email_field, '') or ''

        user_type = user.user_type
        return f"{user.pk}{user.password}{login_timestamp}{timestamp}{email}{user_type}"

    def _make_user_friendly_token(self, email, token):
        """
        Make token as user friendly format
        Adding email for quick attract user information
        @param email:
        @param token:
        @return:
        """
        combined_string = f"{email}:{token}"
        token = base64.b64encode(combined_string.encode()).decode()
        return token

    def extract_token_data(self, token):
        """
        Extract data from token
        @param token:
        @return:
        """
        decoded_string = base64.b64decode(token.encode()).decode()
        email, token = decoded_string.split(':')
        return email, token
