"""Модуль содержит модель для работы с благодарностями.

Модели:
    - Gratitude: Модель для хранения информации о благодарностях
"""

from django.core.validators import FileExtensionValidator
from django.db import models
from ordered_model.models import OrderedModel

from content.constants import (
    EMPTY_VALUE_DISPLAY,
    FILE_CONTENT_TYPES,
    TITLE_LENGTH,
)
from content.mixins import TimestampMixin


class Gratitude(TimestampMixin, OrderedModel):
    """Модель для хранения информации о благодарностях."""

    title = models.CharField(
        verbose_name='Заголовок',
        max_length=TITLE_LENGTH,
        help_text='"Заголовок" не отображается на сайте.',
        blank=True,
        null=True,
    )
    file = models.FileField(
        verbose_name='Файл благодарности',
        upload_to='gratitudes/',
        validators=[FileExtensionValidator(FILE_CONTENT_TYPES)],
    )
    is_active = models.BooleanField('Видимость в ленте', default=True)

    class Meta(OrderedModel.Meta):
        """Класс Meta для модели Gratitude, содержащий мета-данные."""

        verbose_name = 'Благодарность'
        verbose_name_plural = 'Благодарности'
        ordering = [
            'order',
        ]

    def __str__(self):
        """Возвращает строковое представление благодарности."""
        return self.title if self.title is not None else EMPTY_VALUE_DISPLAY
