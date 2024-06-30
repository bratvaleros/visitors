from typing import Union

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from visit_control.departments.models import Department
from visit_control.departments.services.departments.create import CreateDepartmentService
from visit_control.permissions.decorators import Events, check_permissions
from visit_control.utils.handler import BaseHandler
from visit_control.utils.handler_validation_mixin import ValidationMixin
from visit_control.utils.service_object import Ok, Error

User = get_user_model()


class CreateDepartmentHandler(BaseHandler, ValidationMixin):

    @check_permissions(event_code=Events.CREATE_DEPARTMENT)
    def __init__(self, user: User, name: str):
        self.user: User = user
        self.validate(name=name)

    def _clean_name(self, name: str) -> str:
        if len(name) > 100:
            raise self.exception(_("Department name too long"))
        return name

    def run(self) -> Department:
        service: CreateDepartmentService = CreateDepartmentService()
        result: Union[Ok, Error] = service(name=self.validated_data.name)
        if result.is_error():
            raise self.exception(result.error)
        return result.value.department
