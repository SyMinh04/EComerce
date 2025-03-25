import json

from core.system.authentication.backends.authenticators import AuthApplicationBasicAuthentication
from core.system.authentication.reponses import AuthorizedResponse
from core.utils.request import get_portal_type_from_request, get_origin_domain_from_request
from core.views.api import BaseAPIViewSet


class AbstractUserAuthorizationTokenView(BaseAPIViewSet):
    authentication_classes = [AuthApplicationBasicAuthentication]
    serializer = None
    auth_service = None
    is_refresh_token = False

    def get_access_token(self, request):
        """
        Process login using ourselves server
        @param request:
        @return: AccessToken data
        """
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if not self.is_refresh_token:
            return self._login(request, data)

        return self._refresh(request, data)

    def _login(self, request, data):
        """
        Login by user credential
        """
        token_data = self.auth_service.user_credential_login(request, **data)
        return AuthorizedResponse(data=token_data, path=get_portal_type_from_request(request), domain=get_origin_domain_from_request(request))

    def _refresh(self, request, data):
        """
        Refresh access token
        """
        token_data = self.auth_service.renew_access_token(request, **data)
        return AuthorizedResponse(data=token_data, path=get_portal_type_from_request(request), domain=get_origin_domain_from_request(request))

    def get_request_data(self, request):
        """
        Parse request data
        @param request:
        @return:
        """
        form_data = request.POST
        try:
            body_data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            body_data = {}
        return {**body_data, **form_data}
