from typing import Union
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from visit_control.departments.models import Department
from visit_control.departments.services.departments.delete import DeleteDepartmentService
from visit_control.permissions.decorators import Events, check_permissions
from visit_control.utils.handler import BaseHandler
from visit_control.utils.service_object import Ok, Error

User = get_user_model()


class DeleteDepartmentHandler(BaseHandler):

    @check_permissions(event_code=Events.DELETE_DEPARTMENT)
    def __init__(self, user: User, department: Department):
        self.user: User = user
        self.department: Department = department

    def run(self):
        service: DeleteDepartmentService = DeleteDepartmentService()
        result: Union[Ok, Error] = service(self.department)
        if result.is_error():
            raise self.exception(result.error)

    def _prepare_department_id(self, data_handler):
        try:
            return Department.objects.get(pk=data_handler.department_id)
        except Department.DoesNotExist:
            raise self.exception(_("Department not found"))
