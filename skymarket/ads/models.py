from django.conf import settings
from django.db import models

from users.models import User


class Ad(models.Model):
    title = models.CharField(max_length=100, verbose_name="Наименование")
    price = models.PositiveIntegerField(verbose_name="Цена")
    description = models.TextField(max_length=1000, verbose_name="Описание", blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    created_at = models.DateTimeField(
        blank=True, auto_now_add=True, verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объяления"
        ordering = [
            "created_at",
        ]


class Comment(models.Model):
    text = models.TextField(max_length=1000, verbose_name="Отзыв")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name="Товар")
    created_at = models.DateTimeField(
        blank=True, auto_now_add=True, verbose_name="Дата публикации"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = [
            "created_at",
        ]
