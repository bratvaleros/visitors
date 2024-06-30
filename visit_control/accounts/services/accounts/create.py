from typing import Union
from django.contrib.auth import get_user_model
from visit_control.utils.service_object import ServiceObject, transactional, service_call, Error, Ok

Account = get_user_model()


class CreateAccountService(ServiceObject):
    def create_account(self, context):
        account: Account = Account.objects.create(username=context.username, first_name=context.first_name,
                                            is_active=context.is_active, is_superuser=context.is_superuser)
        return self.success(account=account)

    @transactional
    @service_call
    def __call__(self, username: str, first_name: str, is_active: bool, is_superuser: bool) -> Union[Ok, Error]:
        return self.success(username=username, first_name=first_name, is_active=is_active,
                            is_superuser=is_superuser) | self.create_account
