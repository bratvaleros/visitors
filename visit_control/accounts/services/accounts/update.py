from typing import Union

from django.contrib.auth import get_user_model
from visit_control.utils.service_object import ServiceObject, service_call, transactional, Ok, Error

Account = get_user_model()


class UpdateAccountService(ServiceObject):

    def update(self, context):
        account: Account = context.account
        for attr, value in context.params.items():
            setattr(account, attr, value)

        account.save()

        return self.success()

    @transactional
    @service_call
    def __call__(self, account: Account, **kwargs) -> Union[Ok, Error]:
        return self.success(account=account, params=kwargs) | self.update
