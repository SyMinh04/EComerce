from rest_framework import serializers


class UserResetPasswordByTokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
