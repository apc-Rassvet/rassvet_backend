"""Модуль содержит миксины для классов."""

from typing import Optional, Type

from django.db import models

from rest_framework.serializers import Serializer

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


class CleanEmptyHTMLMixin:
    """Миксин для автоматической очистки HTML-полей от "пустых" значений."""

    clean_html_fields: tuple[str, ...] = ()

    def save(self, *args, **kwargs):
        """Переопределяет сохранение объекта: очищает указанные HTML-поля."""
        for field in self.clean_html_fields:
            original_field = getattr(self, field, None)
            setattr(self, field, self._clean_empty_html(original_field))
        super().save(*args, **kwargs)

    def _clean_empty_html(self, raw_html):
        """Проверяет значение HTML-поля.

        Если значение поля ровно <p>&nbsp;</p> (или <p> </p>), возвращает None.
        В остальных случаях возвращает оригинальное значение.
        """
        if raw_html is None:
            return None
        cleared = raw_html.strip().replace('\xa0', '&nbsp;')
        if cleared == '<p>&nbsp;</p>':
            return None
        return raw_html


class MultiSerializerViewSetMixin:
    """Миксин для выбора подходящего сериализатора из `serializer_classes`."""

    serializer_classes: Optional[dict[str, Type[Serializer]]] = None

    def get_serializer_class(self):
        """Выбирает сериализатор из словаря по действию."""
        try:
            return self.serializer_classes[self.action]
        except (KeyError, TypeError):
            return super().get_serializer_class()
