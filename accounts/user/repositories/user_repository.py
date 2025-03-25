from accounts.auth_user.repositories import AuthUserRepository
from accounts.user.models import User
from core.enums.user_type import UserType


class UserRepository(AuthUserRepository):
    user_type = UserType.USER.value
    def __init__(self):
        super().__init__()
        self.model = User
