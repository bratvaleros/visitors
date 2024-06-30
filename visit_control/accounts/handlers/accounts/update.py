from typing import Union

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from visit_control.accounts.services.accounts.update import UpdateAccountService
from visit_control.permissions.decorators import Events, check_permissions
from visit_control.utils.handler import BaseHandler
from visit_control.utils.handler_validation_mixin import ValidationMixin
from visit_control.utils.service_object import Ok, Error

Account = get_user_model()


class UpdateAccountHandler(BaseHandler, ValidationMixin):

    @check_permissions(event_code=Events.UPDATE_ACCOUNT)
    def __init__(self, user: Account, account: Account, **kwargs):
        """
            user - operation requestor User
            account - User record under update
        """
        self.user: Account = user
        self.account: Account = account
        self.validate(**kwargs)  # this call always required

    def run(self) -> Account:
        service: UpdateAccountService = UpdateAccountService()
        result: Union[Ok, Error] = service(account=self.account, **self.validated_data)

        if result.is_error():
            raise self.exception(result.error)

        return self.account

    def _prepare_account_id(self, data_handler):
        try:
            return Account.objects.get(pk=data_handler.account_id)
        except Account.DoesNotExist:
            raise self.exception(_("Account not found"))
