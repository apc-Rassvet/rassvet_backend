"""Модуль содержит модель для работы с отчётами.

Модели:
    - Report: Модель для хранения информации об отчётах
    - Chapter: Модель для хранения информации о разделах отчётов
"""

from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from content.constants import FILE_CONTENT_TYPES


def upload_file(instance, filename):
    """Метод для генерации пути к файлу."""
    return f'reports/{instance.chapter.id}/{filename}'


class Chapter(models.Model):
    """Модель для хранения информации о разделах отчетов."""

    title = models.TextField(verbose_name='Название раздела')
    position = models.PositiveSmallIntegerField(
        default=1, verbose_name='Позиция на странице'
    )

    class Meta:
        """Мета-настройки модели Chapter."""

        verbose_name = 'Раздел отчетов'
        verbose_name_plural = 'Разделы отчетов'
        ordering = ['position']

    def __str__(self):
        """Возвращает строковое представление раздела отчёта."""
        return self.title


class Report(models.Model):
    """Модель для хранения информации о отчетах."""

    title = models.TextField(verbose_name='Название отчета')
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name='Раздел',
    )
    pub_date = models.DateField(
        default=timezone.now,
        verbose_name='Дата публикации',
        help_text='Публикации сортируются от новых к старым',
    )
    file = models.FileField(
        upload_to=upload_file,
        verbose_name='Файл отчета',
        validators=[FileExtensionValidator(FILE_CONTENT_TYPES)],
    )

    class Meta:
        """Мета-настройки модели Report."""

        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'
        ordering = ['-pub_date']

    def __str__(self):
        """Возвращает строковое представление отчёта."""
        return self.title
