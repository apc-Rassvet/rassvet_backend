"""Модуль содержит модель для работы с отзывами.

Модели:
    - Review: Модель для хранения информации об отзывах
"""

from django.db import models

from content.mixins import OrderMixin, TimestampMixin


class Review(OrderMixin, TimestampMixin, models.Model):
    """Модель для хранения информации об отзывах."""

    author_name = models.CharField(
        'Автор',
        max_length=100,
    )
    content = models.TextField('Текст отзыва')
    is_active = models.BooleanField('Активный', default=True)

    class Meta:
        """Класс Meta для модели Review, содержащий мета-данные."""

        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['order', '-created_at']

    def __str__(self):
        """Возвращает строковое представление отзыва."""
        return self.author_name
