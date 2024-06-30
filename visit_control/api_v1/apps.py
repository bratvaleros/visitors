from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ApiV1Config(AppConfig):
    name = "visit_control.api_v1"
    verbose_name = _("API")
