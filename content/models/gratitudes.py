"""Модуль содержит модель для работы с благодарностями.

Модели:
    - Gratitude: Модель для хранения информации о благодарностях
"""

from django.db import models

from content.mixins import OrderMixin, TimestampMixin, TitleMixin


class Gratitude(TitleMixin, OrderMixin, TimestampMixin, models.Model):
    """Модель для хранения информации о благодарностях."""

    file = models.FileField('Файл благодарности', upload_to='gratitudes/')
    is_active = models.BooleanField('Видимость в ленте', default=True)

    class Meta:
        """Класс Meta для модели Gratitude, содержащий мета-данные."""

        verbose_name = 'Благодарность'
        verbose_name_plural = 'Благодарности'
        ordering = ['order', '-created_at']

    def __str__(self):
        """Возвращает строковое представление благодарности."""
        return self.title
