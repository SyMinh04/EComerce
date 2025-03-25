from rest_framework import serializers


class UserBasicInfoSerializer(serializers.Serializer):
    uid = serializers.CharField()
    email = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    user_type = serializers.SerializerMethodField()
