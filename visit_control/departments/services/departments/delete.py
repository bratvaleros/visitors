from typing import Union

from visit_control.departments.models import Department
from visit_control.utils.service_object import ServiceObject, transactional, service_call, Error, Ok


class DeleteDepartmentService(ServiceObject):
    def delete(self, context):
        context.department.delete()
        return self.success()

    @transactional
    @service_call
    def __call__(self, department: Department) -> Union[Ok, Error]:
        return self.success(department=department) | self.delete
