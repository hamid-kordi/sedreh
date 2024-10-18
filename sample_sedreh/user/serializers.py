from rest_framework import serializers
from .models import User


def clean_email(value):
    if "admin" in value:
        raise serializers.ValidationError("admin in email is not accepted")


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("id", "username", "budget", "email", "password", "password2")
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"validators": (clean_email,)},
        }

    def create(self, validated_data):
        del validated_data["password2"]
        return User.objects.create_user(**validated_data)

    def validate_user_name(self, value):
        if value == "admin":
            raise serializers.ValidationError("user name can not be admin")
        return value

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("password 1and 2 not match")
        return data


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")

        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"validators": (clean_email,)},
        }

    def validate_user_name(self, value):
        if value == "admin":
            raise serializers.ValidationError("user name can not be admin")
        return value
