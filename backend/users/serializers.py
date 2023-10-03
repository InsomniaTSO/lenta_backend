
from django.contrib.auth import authenticate
from djoser.serializers import (TokenCreateSerializer, UserCreateSerializer,
                                UserSerializer)
from rest_framework import serializers

from lenta_backend.constants import FORBIDDEN_NAME
from .models import User


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name')


class SignupSerializer(UserCreateSerializer):
    """Сериализатор регистрации пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'email',
                  'first_name', 'last_name',
                  'password')

    def validate_username(self, username):
        """Проверка username на присутствие в списке запрещенных имен."""
        if username.lower() in FORBIDDEN_NAME:
            raise serializers.ValidationError(
                f'Имя {FORBIDDEN_NAME} использовать запрещено!'
            )
        return username


class CustomTokenCreateSerializer(TokenCreateSerializer):
    """Сериализатор получения токена."""

    class Meta:
        model = User
        fields = (
            'email', 'password'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['email'] = serializers.CharField(required=False)

    def validate(self, attrs):
        """Проверка пароля пользователя."""
        password = attrs.get('password')
        params = {'email': attrs.get('email')}
        self.user = authenticate(
            request=self.context.get('request'), **params, password=password
        )
        if not self.user:
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail('invalid_credentials')
        if self.user and self.user.is_active:
            return attrs
        self.fail('invalid_credentials')
