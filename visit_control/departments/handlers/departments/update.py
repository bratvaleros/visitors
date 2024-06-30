from typing import Union
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from visit_control.departments.models import Department
from visit_control.departments.services.departments.update import UpdateDepartmentService
from visit_control.permissions.decorators import Events, check_permissions
from visit_control.utils.handler import BaseHandler
from visit_control.utils.handler_validation_mixin import ValidationMixin
from visit_control.utils.service_object import Ok, Error

User = get_user_model()


class UpdateDepartmentHandler(BaseHandler, ValidationMixin):

    @check_permissions(event_code=Events.UPDATE_DEPARTMENT)
    def __init__(self, user: User, department: Department, **kwargs):
        self.user: User = user
        self.department: Department = department
        self.validate(**kwargs)

    def _clean_name(self, name: str) -> str:
        if len(name) > 100:
            raise self.exception(_("Department name too long"))
        return name

    def run(self) -> Department:
        service: UpdateDepartmentService = UpdateDepartmentService()
        result: Union[Ok, Error] = service(self.department, **self.validated_data)
        if result.is_error():
            raise self.exception(result.error)
        return self.department

    def _prepare_department_id(self, data_handler):
        try:
            return Department.objects.get(pk=data_handler.department_id)
        except Department.DoesNotExist:
            raise self.exception(_("Department not found"))
