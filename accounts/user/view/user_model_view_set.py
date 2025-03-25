from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.user.serializers.user_login_serializer import UserLoginSerializer
from accounts.user.serializers.user_register_serialzier import UserRegistrationSerializer
from accounts.user.service.user_service import UserService


class UserRegisterView(APIView):

    user_service = UserService()

    def post(self, request):
        # serializer = UserRegistrationSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        user = self.user_service.create_user(**request.data)
        return Response({'message': 'User registered successfully', 'user': user},
                        status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request):
        data = self.user_service.