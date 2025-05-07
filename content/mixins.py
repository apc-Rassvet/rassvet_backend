"""Модуль содержит миксины для классов."""

from django.db import models

from .constants import ORDER_DEFAULT, TITLE_LENGTH


class TitleMixin(models.Model):
    """Абстрактная модель для добавления поля заголовка."""

    title = models.CharField('Заголовок', max_length=TITLE_LENGTH)

    class Meta:
        """Мета-класс для указания того, что модель является абстрактной."""

        abstract = True


class TimestampMixin(models.Model):
    """Абстрактная модель для добавления временных меток."""

    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        """Мета-класс для указания того, что модель является абстрактной."""

        abstract = True


class OrderMixin(models.Model):
    """Абстрактная модель для добавления поля порядка отображения."""

    order = models.PositiveSmallIntegerField(
        'Порядок отображения',
        default=ORDER_DEFAULT,
        help_text='Чем меньше значение, тем первее в списке',
    )

    class Meta:
        """Мета-класс для указания того, что модель является абстрактной."""

        abstract = True
