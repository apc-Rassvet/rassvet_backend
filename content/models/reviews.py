"""Модуль содержит модель для работы с отзывами.

Модели:
    - Review: Модель для хранения информации об отзывах
"""

from django.db import models
from ordered_model.models import OrderedModel

from content.mixins import TimestampMixin


class Review(TimestampMixin, OrderedModel):
    """Модель для хранения информации об отзывах."""

    author_name = models.CharField(
        'Автор',
        max_length=100,
    )
    content = models.TextField('Текст отзыва')
    is_active = models.BooleanField('Активный', default=True)

    class Meta(OrderedModel.Meta):
        """Класс Meta для модели Review, содержащий мета-данные."""

        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = [
            'order',
        ]

    def __str__(self):
        """Возвращает строковое представление отзыва."""
        return self.author_name
