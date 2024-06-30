from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from visit_control.permissions.decorators import check_permissions, Events
from visit_control.utils.handler import BaseHandler
from visit_control.utils.utils import QueryType

Account = get_user_model()


class GetAccountsHandler(BaseHandler):

    @check_permissions(event_code=Events.GET_ACCOUNTS)
    def __init__(self, user: Account):
        self.user: Account = user

    @staticmethod
    def run() -> QueryType[Account]:
        return Account.objects.all()


class GetAccountHandler(BaseHandler):

    @check_permissions(event_code=Events.GET_ACCOUNT)
    def __init__(self, user: Account, account: Account):
        self.user: Account = user
        self.account: Account = account

    def run(self) -> Account:
        return self.account

    def _prepare_account_id(self, data_handler):
        try:
            return Account.objects.get(pk=data_handler.account_id)
        except Account.DoesNotExist:
            raise self.exception(_("Account not found"))
