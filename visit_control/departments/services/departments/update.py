from typing import Union

from visit_control.departments.models import Department
from visit_control.utils.service_object import ServiceObject, service_call, transactional, Ok, Error


class UpdateDepartmentService(ServiceObject):

    def update(self, context):
        department: Department = context.client
        for attr, value in context.params.items():
            setattr(department, attr, value)

        department.save()

        return self.success()

    @transactional
    @service_call
    def __call__(self, department: Department, **kwargs) -> Union[Ok, Error]:
        return self.success(department=department, params=kwargs) | self.update
