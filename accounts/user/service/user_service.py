from accounts.user.repositories.user_repository import UserRepository


class UserService:
    model = UserRepository()

    def create_user(self, **kwargs):
        """
        create new user
        :param kwargs:
        :return:
        """
        return self.model.create(**kwargs)

