from typing import Union
from visit_control.departments.models import Department
from visit_control.utils.service_object import ServiceObject, transactional, service_call, Error, Ok


class CreateDepartmentService(ServiceObject):
    def create_client(self, context):
        department: Department = Department.objects.create(name=context.name)
        return self.success(department=department)

    @transactional
    @service_call
    def __call__(self, name:) -> Union[Ok, Error]:
        return self.success(name=name) | self.create_client
