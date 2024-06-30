from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Account(AbstractUser):
    username = models.CharField(_("Логин"), max_length=100, unique=True,
                                help_text=_("Required. Up to 100 characters. Letters, digits, @/./+/-/_ only"),
                                )
    first_name = models.CharField(_("ФИО пользователя"), max_length=150, blank=True)
    last_name = None  # disable field

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = _("Аккаунты")
        verbose_name = _("Аккаунт")
