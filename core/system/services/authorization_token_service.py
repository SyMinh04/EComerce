import base64
from datetime import timedelta
from urllib.parse import unquote_plus

from django.contrib.auth.hashers import check_password
from django.db.models.functions import Now
from django.utils.translation import gettext as _

from core.exception import BadRequest
from core.system.authentication.exceptions.errors import TokenNotFoundError, InvalidClientError, \
    UnsupportedGrantTypeError
from core.system.enums import AuthApplicationGrantType
from core.system.models import AuthApplication
from core.system.repositories import AuthAccessTokenRepository, AuthRefreshTokenRepository
from utils.time import current_time


class AuthorizationTokenService:
    access_token_repo = None
    refresh_token_repo = None
    jwt_settings = None

    def __init__(self):
        self.access_token_repo = AuthAccessTokenRepository()
        self.refresh_token_repo = AuthRefreshTokenRepository()
        # self.jwt_settings = get_jwt_settings()

    def create_access_token(self, request, user, grant_from=None, **kwargs):
        """
        Create access_token grant type password for the given user
        """
        now = Now()
        application = self.get_authenticate_application(request)
        access_token = self.access_token_repo.create(
            user_id=user.uid,
            user_type=user.get_user_type(),
            access_token=self.generate_access_token(request, user),
            application_id=application.uid,
            grant_from=grant_from,
            expires=now + timedelta(seconds=self.jwt_settings.get('ACCESS_TOKEN_LIFETIME')),
            scopes=kwargs.get('scope', None),
            source_refresh_token_id=kwargs.get('refresh_token_id', None),
            mfa_required=user.is_enable_mfa
        )

        refresh_token = self.refresh_token_repo.create(
            user_id=user.uid,
            user_type=user.get_user_type(),
            access_token_id=access_token.uid,
            refresh_token=self.generate_refresh_token(request, user, application),
            application_id=application.uid,
            expires=now + timedelta(seconds=self.jwt_settings.get('REFRESH_TOKEN_LIFETIME'))
        )

        return access_token, refresh_token

    def get_refresh_token(self, token):
        """
        Get Refresh Token
        @param token:
        """
        return self.refresh_token_repo.find_by_token(token)

    def get_access_token(self, token):
        """
        Get access Token
        @param token:
        """
        return self.access_token_repo.find_by_token(token)

    def get_access_token_from_refresh(self, request, refresh_token, scope=None):
        refresh_token = self.get_refresh_token(refresh_token)
        if not refresh_token or refresh_token.is_revoked:
            raise BadRequest(_('invalid_refresh_token'))

        user = get_content_object(refresh_token.user_type, refresh_token.user_id)
        if not user:
            raise BadRequest(_('invalid_refresh_token'))

        access_token = self.access_token_repo.find_by_uid(refresh_token.access_token_id)

        kwargs = {
            'scope': scope,
            'refresh_token_id': refresh_token.uid
        }

        if access_token:
            self.revoke_access_token(access_token)
            self.revoke_refresh_token(refresh_token)

        access_token, refresh_token = self.create_access_token(request, user, AuthApplicationGrantType.REFRESH.value, **kwargs)
        return access_token, refresh_token, user

    def revoke_token(self, request):
        """
        Revoke access token
        @param request:
        """
        access_token = request.auth

        if not access_token:
            raise TokenNotFoundError(request=request)

        self.revoke_access_token(access_token)
        refresh_token = self.refresh_token_repo.find_by_access_token_id(access_token.uid)

        if refresh_token:
            self.revoke_refresh_token(refresh_token)
            return True

        return False

    def revoke_access_token(self, access_token):
        """
        Revoke access token
        @param access_token:
        """
        revoked_at = current_time()
        return self.access_token_repo.update(
            instance=access_token,
            revoked_at=revoked_at,
            is_revoked=True,
        )

    def revoke_refresh_token(self, refresh_token):
        """
        Revoke refresh token
        @param refresh_token:
        """
        revoked_at = current_time()
        return self.refresh_token_repo.update(
            instance=refresh_token,
            revoked_at=revoked_at,
            is_revoked=True,
        )

    def generate_access_token(self, request, user):
        """
        Return a token for the given user.
        @param request: the request issue for this action
        @param user:
        """
        lifetime = self.jwt_settings.get('ACCESS_TOKEN_LIFETIME')
        payload = {
            'user': {
                'uid': str(user.uid),
                'email': str(user.email),
                'user_type': user.get_user_type()
            },
            'iss': request.build_absolute_uri(),
            'iat': current_time().timestamp(),
        }

        jwt_token = create_jwt_token(payload, lifetime)
        return jwt_token.serialize()

    def generate_refresh_token(self, request, user, access_token):
        """
        Return a refresh token for the current access_token.
        """
        lifetime = self.jwt_settings.get('REFRESH_TOKEN_LIFETIME')
        payload = {
            'user': {
                'uid': str(user.uid),
                'email': str(user.email),
                'user_type': user.get_user_type()
            },
            'iss': request.build_absolute_uri(),
            'iat': current_time().timestamp(),
            'auid': str(access_token.uid),
        }

        jwt_token = create_jwt_token(payload, lifetime)
        return jwt_token.serialize()

    def get_authenticate_application(self, request):
        """
        Authenticates application with HTTP Basic Auth.
        @param request:
        @return: Application
        """
        if request and hasattr(request, 'auth_application') and request.auth_application:
            return request.auth_application

        auth_string = self._extract_basic_auth(request)
        if not auth_string:
            raise InvalidClientError(request=request)

        try:
            encoding = request.encoding or 'utf-8'
            b64_decoded = base64.b64decode(auth_string)
            auth_string_decoded = b64_decoded.decode(encoding)
            client_id, client_secret = map(unquote_plus, auth_string_decoded.split(':', 1))
            application = AuthApplication.objects.get(client_id=client_id)
            grant_type = request.data.get('grant_type') or ''

            if not application or not check_password(client_secret, application.client_secret):
                raise InvalidClientError(request=request)

            if application.authorization_grant_type == grant_type:
                return application

            raise UnsupportedGrantTypeError(request=request)

        except Exception:
            raise InvalidClientError(request=request)

    def _extract_basic_auth(self, request):
        """
        Return authenticators string if request contains basic auth credentials,
        otherwise return None
        """
        auth = request.META.get('HTTP_AUTHORIZATION', None)
        if not auth:
            return None

        splitted = auth.split(' ', 1)
        if len(splitted) != 2:
            return None
        auth_type, auth_string = splitted

        if auth_type != 'Basic':
            return None

        return auth_string
