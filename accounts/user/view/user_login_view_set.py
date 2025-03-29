from accounts.user.serializers.user_login_serializer import UserLoginSerializer
from accounts.user.service.user_service import UserService
from core.system.views.api import AbstractUserAuthorizationTokenView


class UserLoginView(AbstractUserAuthorizationTokenView):
    request_serializer = UserLoginSerializer
    auth_service = UserService()
