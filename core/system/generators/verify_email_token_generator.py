from django.utils.crypto import constant_time_compare
from django.utils.http import base36_to_int

from .reset_password_token_generator import AuthUserResetPasswordTokenGenerator


class AuthUserVerifyEmailTokenGenerator(AuthUserResetPasswordTokenGenerator):

    def check_token(self, user, token):
        """
        Check that token is correct for a given user.
        """
        if not (user and token):
            return False
        # Parse the token
        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the timestamp/uid has not been tampered with
        for secret in [self.secret, *self.secret_fallbacks]:
            if constant_time_compare(
                self._make_token_with_timestamp(user, ts, secret),
                token,
            ):
                return True

        return False
