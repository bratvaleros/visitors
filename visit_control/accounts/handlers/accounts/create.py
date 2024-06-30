from typing import Union

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from visit_control.accounts.services.accounts.create import CreateAccountService
from visit_control.permissions.decorators import Events, check_permissions
from visit_control.utils.handler import BaseHandler
from visit_control.utils.service_object import Ok, Error

Account = get_user_model()


class CreateAccountHandler(BaseHandler):

    @check_permissions(event_code=Events.CREATE_ACCOUNT)
    def __init__(self, user: Account, username: str, first_name: str, is_active: bool, is_superuser: bool):
        self.user: Account = user
        self.input_params = [username, first_name, is_active, is_superuser]

    def run(self) -> Account:
        service: CreateAccountService = CreateAccountService()
        result: Union[Ok, Error] = service(*self.input_params)

        if result.is_error():
            raise self.exception(result.error)

        return result.value.account
