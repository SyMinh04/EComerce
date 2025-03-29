from accounts.user.serializers.user_register_serialzier import UserRegistrationSerializer
from accounts.user.service.user_service import UserService
from core.system.views.api import AbstractUserAuthorizationTokenView


class UserRegisterView(AbstractUserAuthorizationTokenView):
    request_serializer = UserRegistrationSerializer
    auth_service = UserService()
