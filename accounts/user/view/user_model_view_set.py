from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from accounts.user.models import User
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
        user = User.objects.filter(id='067e4bf6-1ab5-7638-8000-0e3d52e13876').first()
        refresh = RefreshToken.for_user(user)  # Tạo refresh token
        access_token = str(refresh.access_token)  # Gen access token từ refresh token
        return Response({
            'access_token': access_token,
            'refresh_token': str(refresh),
        }, status=HTTP_200_OK)


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'message': f"Hello , you have accessed a protected view!",
        })