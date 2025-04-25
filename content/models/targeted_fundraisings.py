from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django_ckeditor_5.fields import CKEditor5Field

from content.constants import (
    LENGTH_FUNDRAISING_TITLE,
    LENGTH_FUNDRAISING_STATUS,
)
from content.validators import validate_not_empty_html


class FundraisingStatus(models.TextChoices):
    ACTIVE = 'active', 'Актуальный сбор'
    COMPLETED = 'completed', 'Завершенный сбор'


class TargetedFundraising(models.Model):
    """Модель 'Адресного сбора'."""

    title = models.CharField(
        max_length=LENGTH_FUNDRAISING_TITLE, verbose_name='Заголовок'
    )
    short_description = models.TextField(verbose_name='Краткое описание')
    fundraising_link = models.URLField('Ссылка на сбор')
    status = models.CharField(
        max_length=LENGTH_FUNDRAISING_STATUS,
        choices=FundraisingStatus.choices,
        default=FundraisingStatus.ACTIVE,
        verbose_name='Статус сбора',
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок отображения',
        help_text='Чем меньше значение, тем первее в списке',
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Адресный сбор'
        verbose_name_plural = 'Адресные сборы'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


class FundraisingPhoto(models.Model):
    """Модель 'Фотография' адресного сбора."""

    title = models.CharField(
        max_length=LENGTH_FUNDRAISING_TITLE, verbose_name='Заголовок'
    )
    fundraising = models.ForeignKey(
        TargetedFundraising,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='Адресный сбор',
    )
    image = models.ImageField(
        upload_to='fundraisings/',
        verbose_name='Фотография',
    )
    position = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        verbose_name='Позиция фотографии (1-3)',
    )

    class Meta:
        verbose_name = 'Фотография сбора'
        verbose_name_plural = 'Фотографии сборов'
        ordering = ['position']
        constraints = [
            models.UniqueConstraint(
                fields=['fundraising', 'position'],
                name='unique_photo_position',
            ),
        ]

    def __str__(self):
        return f'Фотография {self.position} для {self.fundraising.title}'


class FundraisingTextBlock(models.Model):
    """Модель 'Текстовый блок' адресного сбора."""

    fundraising = models.ForeignKey(
        TargetedFundraising,
        on_delete=models.CASCADE,
        related_name='text_blocks',
        verbose_name='Адресный сбор',
    )
    content = CKEditor5Field(
        verbose_name='Текстовый блок',
        config_name='default',
        blank=False,
        validators=[validate_not_empty_html],
    )
    position = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        verbose_name='Позиция блока (1-3)',
    )

    class Meta:
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
        return f'Текстовый блок {self.position} для {self.fundraising.title}'
