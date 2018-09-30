from django.contrib.auth.models import User
from rest_framework import serializers

from core.serializers import DynamicFieldsModelSerializer
from .models import Profile


class ProfileSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Profile
        fields = (
            "id",
            "user_id",
            "name",
            "surname",
            "patronymic",
            "phone_number"
        )


class UserSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "email",
            "is_active",
            "profile"
        )
        write_only_fields = ("password",)
        read_only_fields = ("id", "is_active")

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.is_active = False
        user.set_password(validated_data["password"])
        user.save()
        return user
