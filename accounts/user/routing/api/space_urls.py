from django.urls import include, path
from rest_framework import routers

from accounts.user.view import UserRegisterView, UserLoginView

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('register', UserRegisterView.as_view(), name='api_user_register'),  # Corrected
    path('auth/token', UserLoginView.as_view(), name='api_user_auth_authorize'),  # Corrected

    path('', include(router.urls), name='api_user'),
]
