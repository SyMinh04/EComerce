from django.utils.translation import gettext as _
from rest_framework.authentication import BasicAuthentication

from django.contrib.auth.hashers import check_password

from core.exception import AuthenticationFailed
from core.system.services import AuthApplicationService


class AuthApplicationBasicAuthentication(BasicAuthentication):
    def authenticate_credentials(self, client_id, client_password, request=None):
        """
        Authenticate for the application
        with optional request for context.
        """
        service = AuthApplicationService()
        application = service.get_application(client_id)
        match = check_password(client_password, application.client_secret) if application else False

        if not match:
            raise AuthenticationFailed(_('error_client_credentials'))

        request.set_auth_application(application)

        return None, None
