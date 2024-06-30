from django.utils.translation import gettext_lazy as _
from drf_rw_serializers.generics import ListAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, status
from rest_framework.pagination import PageNumberPagination

from visit_control.api_v1.handlers_views import HandlerView
from visit_control.api_v1.departments.serializers import (
    ReadDepartmentSerializer,
    WriteAddDepartmentSerializer,
    WriteGetDepartmentSerializer,
    WriteUpdateDepartmentSerializer,
)
from visit_control.api_v1.serializers import DummyDetailSerializer, DummyDetailAndStatusSerializer
from visit_control.departments.handlers.departments.create import CreateDepartmentHandler
from visit_control.departments.handlers.departments.delete import DeleteDepartmentHandler
from visit_control.departments.handlers.departments.get import GetDepartmentHandler, GetDepartmentsHandler
from visit_control.departments.handlers.departments.update import UpdateDepartmentHandler
from visit_control.departments.models import Department


class CustomSizePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@extend_schema(tags=["Departments"])
@extend_schema_view(
    get=extend_schema(
        summary="Просмотр списка подразделений",
        responses={
            status.HTTP_200_OK: ReadDepartmentSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    )
)
class DepartmentsView(HandlerView, ListAPIView):
    pagination_class = CustomSizePagination
    queryset = Department.objects.none()  # только для swagger схемы
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["name", "parent"]
    ordering_fields = ["id", "name", "parent"]
    ordering = ["id"]

    def get_queryset(self):
        """Получение множества объектов Departments."""
        self.error_text = _("Get Departments error")
        self.read_serializer_class = ReadDepartmentSerializer
        self.response_code = status.HTTP_200_OK
        self.handler = GetDepartmentsHandler
        return self.get_handler_result()


@extend_schema(tags=["Departments"])
@extend_schema_view(
    post=extend_schema(
        summary="Добавление подразделения",
        request=WriteAddDepartmentSerializer,
        responses={
            status.HTTP_201_CREATED: ReadDepartmentSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    ),
    get=extend_schema(exclude=True),
)
class AddDepartmentView(HandlerView):
    def post(self, request, *args, **kwargs):
        """ Создание записи """
        self.serializer_class = WriteAddDepartmentSerializer
        self.error_text = _("Create Department error")
        self.read_serializer_class = ReadDepartmentSerializer
        self.response_code = status.HTTP_201_CREATED
        self.handler = CreateDepartmentHandler
        return self.handle()


@extend_schema(tags=["Departments"])
class DepartmentView(HandlerView):
    @extend_schema(
        summary="Данные указанного подразделения",
        request=WriteGetDepartmentSerializer,
        responses={
            status.HTTP_200_OK: ReadDepartmentSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        """ Получение информации о записи """
        self.response_code = status.HTTP_200_OK
        self.serializer_class = WriteGetDepartmentSerializer
        self.error_text = _("Get Client error")
        self.read_serializer_class = ReadDepartmentSerializer
        self.handler = GetDepartmentHandler
        return self.handle()

    @extend_schema(
        summary="Обновление данных указанного подразделения. Возможно частичное",
        request=WriteUpdateDepartmentSerializer,
        responses={
            status.HTTP_200_OK: ReadDepartmentSerializer,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        """ Изменение записи """
        self.response_code = status.HTTP_200_OK
        self.serializer_class = WriteUpdateDepartmentSerializer
        self.read_serializer_class = ReadDepartmentSerializer
        self.error_text = _("Update Department error")
        self.handler = UpdateDepartmentHandler
        return self.handle()

    @extend_schema(
        summary="Удаление указанного подразделения",
        request=WriteGetDepartmentSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_400_BAD_REQUEST: DummyDetailSerializer,
            status.HTTP_401_UNAUTHORIZED: DummyDetailSerializer,
            status.HTTP_403_FORBIDDEN: DummyDetailAndStatusSerializer,
        },
    )
    def delete(self, request, *args, **kwargs):
        """ Удаление записи """
        self.response_code = status.HTTP_204_NO_CONTENT
        self.serializer_class = WriteGetDepartmentSerializer
        self.error_text = _("Delete Department error")
        self.handler = DeleteDepartmentHandler
        return self.handle()
