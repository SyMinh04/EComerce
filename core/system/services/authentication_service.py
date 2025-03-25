from django.utils.translation import gettext as _

from accounts.auth_user.models import AuthUser
from core.system.authentication.enums import AuthApplicationGrantType
from core.system.authentication.services.authorization_token_service import AuthorizationTokenService
from core.exceptions import AuthenticationFailed


class AuthenticationService:
    auth_model = AuthUser
    check_active = True

    def user_credential_login(self, request, username: str, password: str, scope: str=None, **kwargs):
        """
        User login from username password
        """
        if username is None:
            username = kwargs.get(self.auth_model.USERNAME_FIELD)
        if username is None or password is None:
            return

        try:
            # Check if the input is an email address
            if '@' in username:
                user = self.auth_model.objects.get(email=username, is_deleted=False)
            else:
                # If not an email, check for username
                user = self.auth_model.objects.get(username=username, is_deleted=False)

            if user is None:
                raise AuthenticationFailed(_('error_invalid_login_credentials'))

            if self.check_active and not user.is_active:
                raise AuthenticationFailed(_('error_user_inactive_or_deleted'))

            if user.get_user_type() != scope:
                raise AuthenticationFailed(_('invalid_user_scope'))

        except self.auth_model.DoesNotExist:
            raise AuthenticationFailed(_('error_invalid_login_credentials'))

        if user.check_password(password):
            return self.create_authorization_token(request, user, scope=scope, **kwargs)

        raise AuthenticationFailed(_('error_invalid_login_credentials'))

    def create_authorization_token(self, request, user, **kwargs):
        """
        Create token for login session
        """
        authorization_token_service = AuthorizationTokenService()
        access_token, refresh_token = authorization_token_service.create_access_token(
            request,
            user,
            grant_from=AuthApplicationGrantType.PASSWORD.value,
            scope=kwargs.get('scope', self.auth_model.__user_type__),
        )

        return {
            'access_token': access_token.access_token,
            'refresh_token': refresh_token.refresh_token,
            'token_type': 'Bearer',
            'mfa_required': user.is_enable_mfa
        }

    def renew_access_token(self, request, refresh_token: str,  scope: str=None, **kwargs):
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
