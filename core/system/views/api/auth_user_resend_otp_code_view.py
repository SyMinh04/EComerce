# from django.contrib.auth.models import AnonymousUser
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.translation import gettext as _
# from rest_framework import status
# from rest_framework.response import Response
#
# from accounts.staff.services.auth.staff_user_mfa_service import StaffMFAService
# from core.views.api import BaseAPIViewSet
# from core.system.authentication.backends.authenticators import AcceptNotConfirmMFAAuthentication
#
#
# class AuthUserResendOTPCodeView(BaseAPIViewSet):
#     authentication_classes = [AcceptNotConfirmMFAAuthentication]
#
#     @csrf_exempt
#     def resend_mfa_email_otp_code(self, request):
#         """
#         Resend MFA code to user's email address.
#         @param request:
#         @return:
#         """
#         user = request.user
#
#         if isinstance(user, AnonymousUser):
#             return Response({'detail': _('error_user_not_login')}, status=status.HTTP_401_UNAUTHORIZED)
#
#         if request.auth and hasattr(request, 'auth') and request.auth.is_mfa_verified:
#             return Response({'detail': _('error_mfa_already_verified')}, status=status.HTTP_400_BAD_REQUEST)
#
#         user_mfa_service = StaffMFAService()
#         user_mfa_service.resend_email_otp_code(user)
#
#         return Response({'detail': _('message_otp_resent')}, status=status.HTTP_200_OK)
