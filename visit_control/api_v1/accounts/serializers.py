from dj_rest_auth.serializers import LoginSerializer as DefaultLoginSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class LoginSerializer(DefaultLoginSerializer):
    username = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)
    email = None

    def validate(self, attrs):
        username: str = attrs.get("username")
        password: str = attrs.get("password")
        user = self._validate_username(username, password)
        if not user or not user.is_active:
            raise AuthenticationFailed()

        attrs["user"] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value: str):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError(detail=_("Invalid password"))

        return value

    def validate_new_password(self, value: str):
        validate_password(value)
        return value

    def validate(self, attrs):
        if attrs.get("new_password") == attrs.get("old_password"):
            raise serializers.ValidationError(
                {"new_password": _("The new password cannot be the same as the old password")},
            )

        return attrs


class ReadAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "is_active", "is_superuser", "last_login")


class WriteAddAccountSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, label=_("username"))
    first_name = serializers.CharField(max_length=150, label=_("first_name"))
    is_active = serializers.BooleanField(default=True)
    is_superuser = serializers.BooleanField(default=False)


class WriteGetAccountSerializer(serializers.Serializer):
    pass


class WriteUpdateAccountSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=False)
    first_name = serializers.CharField(max_length=150, required=False)
    is_active = serializers.BooleanField(required=False)
    is_superuser = serializers.BooleanField(required=False)


class SetAccountPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    account_id = serializers.IntegerField(required=True)

    def validate_new_password(self, value: str):
        validate_password(value)
        return value
