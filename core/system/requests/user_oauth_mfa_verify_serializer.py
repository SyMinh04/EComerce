from rest_framework import serializers


class UserMFAVerifySerializer(serializers.Serializer):
    verify_code = serializers.CharField(required=True, max_length=255)

