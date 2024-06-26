from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db import models
from users.managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class UserRoles(models.TextChoices):
        USER = "1", "USER"
        ADMIN = "2", "ADMIN"

    username = None
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    phone = PhoneNumberField(verbose_name="Телефон")
    email = models.EmailField(max_length=75, verbose_name="Почта", unique=True, default="example@example.com")
    role = models.CharField(
        choices=UserRoles.choices, default=UserRoles.USER, verbose_name="Роль"
    )
    image = models.ImageField(verbose_name="Аватар", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = [
            "id",
        ]
