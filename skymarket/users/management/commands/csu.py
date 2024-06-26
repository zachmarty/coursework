from typing import Any
from django.core.management import BaseCommand
from users.models import User
from rest_framework.exceptions import NotFound

class Command(BaseCommand):
    """Команда для создания суперпользователя"""
    def handle(self, *args: Any, **options: Any) -> str | None:
        admin = User.objects.create(
            email="admin@mail.ru",
            first_name="admin",
            last_name="admin",
            is_staff=True,
            is_superuser=True,
            phone = "+1234567890",
            role = 2,
        )
        admin.set_password("12345678")
        admin.save()
