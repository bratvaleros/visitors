from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Department(models.Model):

    name = models.CharField(max_length=100, verbose_name=_("Наименование подразделения"))
    parent = models.ForeignKey('self', verbose_name=_("Входит в состав"), on_delete=models.CASCADE,
                               blank=True, null=True, related_name="departments")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Подразделение")
        verbose_name_plural = _("Подразделения")
