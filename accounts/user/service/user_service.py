from accounts.user.repositories.user_repository import UserRepository
from core.system.services import AuthenticationService


class UserService(AuthenticationService):
    auth_model = UserRepository()

