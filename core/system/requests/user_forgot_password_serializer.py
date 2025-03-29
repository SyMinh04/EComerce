from rest_framework import serializers



class UserForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
