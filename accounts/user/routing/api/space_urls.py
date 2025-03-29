from django.urls import path
from rest_framework import routers

from accounts.user.view import UserRegisterView
from accounts.user.view.user_login_view_set import UserLoginView

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('register', UserRegisterView.as_view({'post': 'create_user'}), name='api_user_auth_authorize'),
    path('auth/token', UserLoginView.as_view({'post': 'get_access_token'}), name='api_user_auth_authorize'),
]
