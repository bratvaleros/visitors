from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountsConfig(AppConfig):
    name = "visit_control.accounts"
    verbose_name = _("Управление аккаунтами")
