from django.apps import AppConfig


class AuthUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts.auth_user'
    label = 'account_auth_user'
    verbose_name = 'User Management'
