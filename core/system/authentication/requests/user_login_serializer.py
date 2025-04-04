from rest_framework import serializers


class UserLoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, max_length=255)
    grant_type = serializers.CharField(required=True, max_length=255)
    scope = serializers.CharField(required=True, max_length=255)

    class Meta:
        fields = ['username', 'password', 'grant_type', 'scope']
