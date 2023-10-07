from djoser import utils
from djoser.serializers import TokenSerializer
from djoser.views import TokenCreateView
from rest_framework import status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST)

from .models import User
from .serializers import CustomUserSerializer, SignupSerializer


class CustomTokenCreateView(TokenCreateView):
    """Вьюсет получения токена."""
    def _action(self, serializer):
        """Возвращает токен и статус HTTP_201_CREATED."""
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = TokenSerializer
        return Response(
            data=token_serializer_class(token).data,
            status=status.HTTP_201_CREATED
        )


class CustomUserViewSet(viewsets.ModelViewSet):
    """Вьюсет пользователей."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        """
        Возвращает сериализатор в зависимости от
        используемого метода.
        """
        if self.action == "create":
            return SignupSerializer
        return self.serializer_class


