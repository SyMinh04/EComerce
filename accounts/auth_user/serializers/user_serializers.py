from accounts.auth_user.models import AuthUser


class UserSerializer:
    class Meta:
        model = AuthUser
        fields = '__all__'
