from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PermissionsConfig(AppConfig):
    name = "visit_control.permissions"
    verbose_name = _("Управление доступом к событиям")
