"""Модуль содержит модели, связанные с адресными сборами.

Классы:
    FundraisingStatus: Перечисление возможных статусов для адресного сбора.

Модели:
    1. TargetedFundraising: Модель для хранения информации об адресном сборе
    2. FundraisingPhoto: Модель для хранения фотографий адресных сборов
    3. FundraisingTextBlock: Модель для хранения текстовых блоков
       адресных сборов
"""

from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from ordered_model.models import OrderedModel

from content.constants import IMAGE_CONTENT_TYPES
from content.mixins import TimestampMixin, TitleMixin
from content.validators import validate_not_empty_html


def upload_file(instance, filename):
    """Генерирует путь к файлу для загрузки."""
    return f'fundraisings/{instance.fundraising.id}/{filename}'


class FundraisingStatus(models.TextChoices):
    """Класс, определяющий возможные статусы адресного сбора."""

    ACTIVE = 'active', 'Актуальный сбор'
    COMPLETED = 'completed', 'Завершенный сбор'


class TargetedFundraising(
    TitleMixin,
    TimestampMixin,
    OrderedModel,
):
    """Модель для хранения информации об адресных сборах."""

    short_description = models.TextField(verbose_name='Краткое описание')
    fundraising_link = models.URLField('Ссылка на сбор')
    status = models.CharField(
        max_length=max(len(value) for value, _ in FundraisingStatus.choices),
        choices=FundraisingStatus.choices,
        default=FundraisingStatus.ACTIVE,
        verbose_name='Статус сбора',
    )

    class Meta(OrderedModel.Meta):
        """Класс Meta для TargetedFundraising, содержащий мета-данные."""

        verbose_name = 'Адресный сбор'
        verbose_name_plural = 'Адресные сборы'
        ordering = [
            'order',
        ]

    def __str__(self):
        """Возвращает строковое представление адресного сбора."""
        return self.title


class FundraisingPhoto(OrderedModel):
    """Модель для хранения информации о фотографиях адресных сборов."""

    fundraising = models.ForeignKey(
        TargetedFundraising,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='Адресный сбор',
    )
    image = models.ImageField(
        upload_to=upload_file,
        verbose_name='Фотография',
        validators=[FileExtensionValidator(IMAGE_CONTENT_TYPES)],
    )
    # position = models.PositiveSmallIntegerField(
    #     default=1,
    #     validators=[MinValueValidator(1), MaxValueValidator(3)],
    #     verbose_name='Позиция фотографии (1-3)',
    # )
    order_with_respect_to = 'fundraising'

    class Meta(OrderedModel.Meta):
        """Класс Meta для FundraisingPhoto, содержащий мета-данные."""

        verbose_name = 'Фотография сбора'
        verbose_name_plural = 'Фотографии сборов'
        ordering = [
            'order',
        ]
        indexes = [
            models.Index(fields=['fundraising', 'order']),
        ]
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=['fundraising', 'position'],
        #         name='unique_photo_position',
        #     ),
        # ]

    def __str__(self):
        """Возвращает строковое представление фотографии."""
        return f'Фотография для {self.fundraising.title}'


class FundraisingTextBlock(models.Model):
    """Модель для хранения информации о текстовых блоках адресных сборов."""

    fundraising = models.ForeignKey(
        TargetedFundraising,
        on_delete=models.CASCADE,
        related_name='text_blocks',
        verbose_name='Адресный сбор',
    )
    content = CKEditor5Field(
        verbose_name='Текстовый блок',
        config_name='default',
        validators=[validate_not_empty_html],
    )
    position = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        verbose_name='Позиция блока (1-3)',
    )

    class Meta:
        """Класс Meta для FundraisingTextBlock, содержащий мета-данные."""

        verbose_name = 'Текстовый блок'
        verbose_name_plural = 'Текстовые блоки'
        ordering = ['position']
        constraints = [
            models.UniqueConstraint(
                fields=['fundraising', 'position'],
                name='unique_text_position',
            ),
        ]

    def __str__(self):
        """Возвращает строковое представление текстового блока."""
        return f'Текстовый блок {self.position} для {self.fundraising.title}'
