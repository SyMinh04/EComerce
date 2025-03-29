from rest_framework import serializers


class UserRegisterRequestSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    password = serializers.CharField(required=True, min_length=8)

