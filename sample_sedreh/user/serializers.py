from rest_framework import serializers
from .models import User, Library, OtpCode


def clean_email(value):
    if "admin" in value:
        raise serializers.ValidationError("admin in email is not accepted")


class UserShowDtat(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "budget", "password", "password2")
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"validators": (clean_email,)},
        }

    def create(self, validated_data):
        del validated_data["password2"]
        return User.objects.create_user(**validated_data)

    def validate_username(self, value):
        if value == "admin":
            raise serializers.ValidationError("user name can not be admin")
        return value

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("password 1and 2 not match")
        return data

    def validate_email(self, value):
        if User.objects.get(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value


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


class OtpCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpCode
        fields = ("user", "code", "created", "price", "expiration_date")


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ("user", "book")


class IncreaseBudgetSerializer(serializers.Serializer):
    user = serializers.IntegerField(required=True)
    code = serializers.IntegerField(required=True)


class BuyBookSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    book_id = serializers.IntegerField(required=True)


class RuternSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    bookId = serializers.IntegerField(required=True)
