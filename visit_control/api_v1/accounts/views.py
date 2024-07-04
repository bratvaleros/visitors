from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, login, logout
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_rw_serializers.generics import ListAPIView
from rest_framework import permissions, status, filters, serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from visit_control.api_v1.accounts.serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    ReadAccountSerializer,
    WriteGetAccountSerializer,
    WriteAddAccountSerializer,
    WriteUpdateAccountSerializer,
    SetAccountPasswordSerializer,
)
from visit_control.api_v1.serializers import DummyDetailAndStatusSerializer, DummyDetailSerializer, EmptySerializer
from visit_control.api_v1.handlers_views import HandlerView
from visit_control.accounts.handlers.accounts.get import GetAccountsHandler, GetAccountHandler
from visit_control.accounts.handlers.accounts.create import CreateAccountHandler
from visit_control.accounts.handlers.accounts.update import UpdateAccountHandler


User = get_user_model()


class CustomSizePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# region api_docs
@extend_schema(tags=["Accounts"])
@extend_schema_view(
    get=extend_schema(
        summary="Данные о текущем пользователе",
        responses={
            status.HTTP_200_OK: ReadAccountSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    ),
)
# endregion
class GetMeView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(
            status=status.HTTP_200_OK,
            data=ReadAccountSerializer(request.user).data,
        )


# region api_docs
@extend_schema(tags=["Accounts"])
@extend_schema_view(
    post=extend_schema(
        summary="Вход в учетную запись",
        responses={
            status.HTTP_200_OK: DummyDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailAndStatusSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
        request=LoginSerializer,
    ),
)
# endregion
class LoginView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=self.request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        login(request, user)
        return JsonResponse({"detail": "Success"})


# region api_docs
@extend_schema(tags=["Accounts"])
@extend_schema_view(
    post=extend_schema(
        summary="Выход из учетной записи",
        responses={
            status.HTTP_200_OK: DummyDetailSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailAndStatusSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    ),
)
# endregion
class LogoutView(GenericAPIView):
    serializer_class = EmptySerializer

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_200_OK)


# region api_docs
@extend_schema(tags=["Accounts"])
@extend_schema_view(
    post=extend_schema(
        summary="Смена пароля",
        responses={
            status.HTTP_200_OK: EmptySerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailSerializer,
        },
    ),
)
# endregion
class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        current_user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_user.set_password(serializer.data.get("new_password"))
        current_user.save()

        return Response(status=status.HTTP_200_OK)


@extend_schema(tags=["Accounts"])
@extend_schema_view(
    get=extend_schema(
        summary="Просмотр списка аккаунтов",
        responses={
            status.HTTP_200_OK: ReadAccountSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    )
)
class AccountsView(HandlerView, ListAPIView):
    pagination_class = CustomSizePagination
    queryset = User.objects.none()  # только для swagger схемы
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["username", "first_name"]
    ordering_fields = ["id", "username"]
    ordering = ["id"]

    def get_queryset(self):
        """Получение множества объектов Users."""
        self.error_text = _("Get Users error")
        self.read_serializer_class = ReadAccountSerializer
        self.response_code = status.HTTP_200_OK
        self.handler = GetAccountsHandler
        return self.get_handler_result()


@extend_schema(tags=["Accounts"])
@extend_schema_view(
    get=extend_schema(exclude=True),
    post=extend_schema(
        summary="Добавление аккаунта",
        request=WriteAddAccountSerializer,
        responses={
            status.HTTP_201_CREATED: ReadAccountSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    ),
)
class CreateAccountView(HandlerView, ListAPIView):
    def post(self, request, *args, **kwargs):
        """ Создание записи """
        self.serializer_class = WriteAddAccountSerializer
        self.error_text = _("Create Account error")
        self.response_code = status.HTTP_201_CREATED
        self.handler = CreateAccountHandler
        return self.handle()


@extend_schema(tags=["Accounts"])
class AccountView(HandlerView):
    @extend_schema(
        summary="Данные указанного аккаунта",
        request=WriteGetAccountSerializer,
        responses={
            status.HTTP_200_OK: ReadAccountSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        """ Получение информации о записи """
        self.response_code = status.HTTP_200_OK
        self.serializer_class = WriteGetAccountSerializer
        self.error_text = _("Get Account error")
        self.read_serializer_class = ReadAccountSerializer
        self.handler = GetAccountHandler
        return self.handle()

    @extend_schema(
        summary="Обновление данных указанного аккаунта. Возможно частичное.",
        request=WriteUpdateAccountSerializer,
        responses={
            status.HTTP_200_OK: ReadAccountSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        """ Изменение записи """
        self.response_code = status.HTTP_200_OK
        self.serializer_class = WriteUpdateAccountSerializer
        self.read_serializer_class = ReadAccountSerializer
        self.error_text = _("Update Account error")
        self.handler = UpdateAccountHandler
        return self.handle()


@extend_schema(tags=["Accounts"])
@extend_schema_view(
    post=extend_schema(
        summary="Назначение пароля любому аккаунту",
        responses={
            status.HTTP_200_OK: EmptySerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailSerializer,
        },
    ),
)
# endregion
class SetAccountPasswordView(GenericAPIView):
    serializer_class = SetAccountPasswordSerializer

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise serializers.ValidationError(detail=_("Operation available for superusers only!"))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        surgery_account = User.objects.get(pk=request.data["account_id"])
        surgery_account.set_password(serializer.data.get("new_password"))
        surgery_account.save()
        return Response(status=status.HTTP_200_OK)
