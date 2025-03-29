from django.utils.translation import gettext as _

from core.exception import AuthenticationFailed
from core.system.enums import AuthApplicationGrantType
from core.system.services.authorization_token_service import AuthorizationTokenService


class AuthenticationService:
    auth_model = None
    check_active = True

    def user_credential_login(self, request, login_data, **kwargs):
        """
        User credential login
        :param request:
        :param login_data:
        :param kwargs:
        :return:
        """
        try:
            user_name, password, scope, grant_type = self._get_login_data(login_data)
            account = None
            if '@' in user_name:
                account = self.auth_model.filter(email=user_name).first()
            else:
                account = self.auth_model.filter(username=user_name).first()
            if account is None:
                raise AuthenticationFailed(_('error_invalid_login_credentials'))

            if not account.is_active:
                raise AuthenticationFailed(_('error_user_inactive_or_deleted'))

            if account.get_user_type() != scope:
                raise AuthenticationFailed(_('invalid_user_scope'))

            if not account.verify_password(password):
                raise AuthenticationFailed(_('error_invalid_login_credentials'))

            return self.create_authorization_token(request, account, scope=scope, **kwargs)
        except Exception as e:
            raise AuthenticationFailed(_('error_invalid_login_credentials'))

    def _get_login_data(self, login_data):
        """
        Get login data
        :param login_data:
        :return:
        """
        return login_data['username'], login_data['password'], login_data['scope'], login_data['grant_type']

    def create_authorization_token(self, request, user, **kwargs):
        """
        Create token for login session
        """
        authorization_token_service = AuthorizationTokenService()
        access_token, refresh_token = authorization_token_service.create_access_token(
            request,
            user,
            grant_from=AuthApplicationGrantType.PASSWORD.value,
            kwargs=kwargs
        )

        return {
            'access_token': access_token.access_token,
            'refresh_token': refresh_token.refresh_token,
            'token_type': 'Bearer',
            'mfa_required': user.is_enable_mfa
        }

    def renew_access_token(self, request, refresh_token: str, scope: str = None, **kwargs):
        authorization_token_service = AuthorizationTokenService()
        access_token, refresh_token, user = authorization_token_service.get_access_token_from_refresh(
            request,
            refresh_token,
            scope
        )

        return {
            'access_token': access_token.access_token,
            'refresh_token': refresh_token.refresh_token,
            'token_type': 'Bearer',
            'mfa_required': access_token.mfa_required
        }

    def user_logout(self, request):
        """
        User logout
        """
        authorization_token_service = AuthorizationTokenService()
        return authorization_token_service.revoke_token(request)

    def create_user(self, request):
        """
        Create new user
        :param request:
        :return:
        """
        return self.auth_model.create(**request)
