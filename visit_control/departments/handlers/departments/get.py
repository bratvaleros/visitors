from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from visit_control.departments.models import Department
from visit_control.permissions.decorators import check_permissions, Events
from visit_control.utils.handler import BaseHandler
from visit_control.utils.utils import QueryType

User = get_user_model()


class GetDepartmentsHandler(BaseHandler):

    @check_permissions(event_code=Events.GET_DEPARTMENTS)
    def __init__(self, user: User):
        self.user: User = user

    def run(self) -> QueryType[Department]:
        return Department.objects.all()


class GetDepartmentHandler(BaseHandler):

    @check_permissions(event_code=Events.GET_DEPARTMENT)
    def __init__(self, user: User, department: Department):
        self.user: User = user
        self.department: Department = department

    def run(self) -> Department:
        return self.department

    def _prepare_department_id(self, data_handler):
        try:
            return Department.objects.get(pk=data_handler.department_id)
        except Department.DoesNotExist:
            raise self.exception(_("Department not found"))
