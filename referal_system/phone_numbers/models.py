from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import HammerSystemManager


class HammerSystemUser(AbstractBaseUser):
    phone = PhoneNumberField("Номер телефона", unique=True)
    auth_code = models.CharField("Код авторизации", max_length=4, null=True)
    invite_code = models.CharField("Инвайт код", max_length=6)
    is_superuser = models.BooleanField("Суперпользователь", default=False)
    invite_code_changed = models.BooleanField(default=False)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = HammerSystemManager()

    def __str__(self) -> str:
        return self.name
