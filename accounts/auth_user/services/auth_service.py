from accounts.user.repositories.user_repository import UserRepository

from django.utils.translation import gettext as _

from core.exception import AuthenticationFailed


class AuthService:
    repo = None

    def user_credential_login(self, request, user_name, password, scope: str = None, **kwargs):
        """
        User credential login
        :param request:
        :param user_name:
        :param password:
        :param scope:
        :param kwargs:
        :return:
        """
        try:
            account = None
            if '@' in user_name:
                account = self.repo.filter(email=user_name).first()
            else:
                account = self.repo.filter(username=user_name).first()
            if account is None:
                raise AuthenticationFailed(_('error_invalid_login_credentials'))

            if not account.is_active:
                raise AuthenticationFailed(_('error_user_inactive_or_deleted'))

            if account.get_user_type() != scope:
                raise AuthenticationFailed(_('invalid_user_scope'))

            if not account.verify_password(password):
                raise AuthenticationFailed(_('error_invalid_login_credentials'))

            return
        except Exception as e:
            raise AuthenticationFailed(_('error_invalid_login_credentials'))
