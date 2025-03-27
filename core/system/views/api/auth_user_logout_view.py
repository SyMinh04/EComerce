from django.utils.translation import gettext as _
from rest_framework import status




class AuthUserLogoutView(BaseProtectedApiView):
    authentication_classes = [AcceptInActiveAuthentication]

    def post(self, request):
        """
        User logout
        @param request:
        @return:
        """
        # Revoke the access token.
        if request.auth and isinstance(request.auth, AuthUserAccessToken):
            service = AuthenticationService()
            service.user_logout(request)

            response = AuthorizedResponse({'detail': _('message_user_logout_successfully')}, status=status.HTTP_200_OK)
        else:
            response = AuthorizedResponse({'detail': _('error_access_token_not_found')}, status=status.HTTP_400_BAD_REQUEST)
        response.clean_authorized_cookies()

        return response
