from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from core.repositories import BaseRepository
from accounts.auth_user.models import AuthUser


class AuthUserRepository(BaseRepository):
    user_type = None

    def __init__(self):
        self.model = AuthUser

    def create(self, **kwargs):
        """
        Create user
        @param kwargs:
        @return:
        """
        kwargs['user_type'] = self.user_type
        # if kwargs.get('password'):
        #     kwargs['password'] = make_password(kwargs['password'])
        return super().create(**kwargs)

    def find_by_email(self, email, is_active=None):
        """
        Find admin user by email
        @param is_active:
        @param email:
        @return:
        """
        arg = {
            'email': email
        }
        if is_active is not None:
            arg['is_active'] = is_active

        return self.filter(**arg).first()

    def reset_user_password(self, user, password):
        """
        Reset new password for user.
        last_login will be updated to make reset token is used
        @param user:
        @param password:
        @return:
        """
        user.set_password(password)
        user.last_login = now()
        user.save()
        return user

    def init_user_password(self, user, password):
        """
        Initial user's password.
        @param user:
        @param password:
        @return:
        """
        user.set_password(password)
        user.save()
        return user

    def get_count(self):
        """
        Get count of users.
        @return:
        """
        return self.all().count()
