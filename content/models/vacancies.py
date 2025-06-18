"""Модуль содержит модели, связанные с вакансиями.

Классы:
    RedirectChoises: Перечисление возможных статусов для типа перехода.

Модели:
    1. Vacancy: содержит информацию о вакансиях.
"""
from django.db import models
from django.core.validators import FileExtensionValidator

from content.constants import IMAGE_CONTENT_TYPES
from content.mixins import TimestampMixin
from content.utils import ckeditor_function


class Vacancy(TimestampMixin, models.Model):
    """Модель вакансий."""

    class RedirectChoises(models.TextChoices):
        DETAIL = 'detail', 'На страницу "Вакансии_подробная"'
        FORM = 'form', 'На форму "Форма регистрации и отклика"'

    profession = models.CharField(max_length=200, verbose_name='Профессия')
    photo = models.ImageField(
        upload_to='vacancies/photos/',
        verbose_name='Фотография',
        validators=[FileExtensionValidator(IMAGE_CONTENT_TYPES)],
    )
    salary = models.CharField(max_length=200, verbose_name='Зарплата')
    short_description = models.TextField(
        max_length=500, verbose_name='Краткий текст'
    )
    schedule = models.CharField(
        max_length=200, blank=True, verbose_name='График'
    )
    location = models.CharField(
        max_length=200, blank=True, verbose_name='Место'
    )
    redirect_type = models.CharField(
        max_length=10,
        choices=RedirectChoises.choices,
        default=RedirectChoises.DETAIL,
        verbose_name='Тип перехода',
    )
    additional_description = ckeditor_function(
        verbose_name='Дополнительное описание'
    )
    detailed_description = ckeditor_function(verbose_name='Описание вакансии')
    external_link = models.URLField(
        blank=True, verbose_name='Ссылка на внешнюю платформу'
    )

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-created_at']

    def __str__(self):
        """Возвращает строковое представление вакансии."""
        return self.profession

    @property
    def has_external_link(self):
        """Есть ли ссылка на внешнюю платформу."""
        return bool(self.external_link)
