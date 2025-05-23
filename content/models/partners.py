"""Модуль содержит модель для работы с партнёрами.

Модели:
    - Partner: Модель для хранения информации о партнёрах
"""

from django.db import models

from content.mixins import OrderMixin, TimestampMixin


class Partner(OrderMixin, TimestampMixin, models.Model):
    """Модель для хранения информации о партнёрах."""

    name = models.CharField(
        max_length=255,
        verbose_name='Название партнера',
    )
    logo = models.ImageField(
        upload_to='partners/logos/',
        verbose_name='Логотип партнера',
    )
    description = models.TextField(
        verbose_name='Описание',
    )

    class Meta:
        """Класс Meta для модели Partner, содержащий мета-данные."""

        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'
        ordering = ['name']

    def __str__(self):
        """Возвращает строковое представление партнёра."""
        return self.name
