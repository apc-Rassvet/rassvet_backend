import html

from django.db import models
from django.utils.html import strip_tags

from django_ckeditor_5.fields import CKEditor5Field

from content.validators import validate_not_empty_html


def upload_file(instance, filename):
    """Метод для генерации пути к файлу."""
    return f'team/{instance.employee.id}/{filename}'


class Employee(models.Model):
    """Модель для хранения информации о членах команды."""

    name = models.CharField(max_length=255, verbose_name='ФИО')
    image = models.ImageField(upload_to='team', verbose_name='Фото')
    main_specialities = CKEditor5Field(
        verbose_name='Специальности на общей странице',
        config_name='default',
        blank=False,
        validators=[validate_not_empty_html],
    )
    order = models.PositiveIntegerField(
        verbose_name='Позиция на общей странице', default=1
    )
    interviews = models.URLField(verbose_name='Интервью', blank=True)
    specialists_register = models.URLField(
        verbose_name='Реестр специалистов', blank=True
    )
    category_on_main = models.BooleanField(
        default=False,
        verbose_name='Отображать категории документов на главной странице',
    )
    specialities = CKEditor5Field(
        verbose_name='Специальности',
        config_name='default',
        blank=False,
        validators=[validate_not_empty_html],
    )
    education = CKEditor5Field(
        verbose_name='Образование',
        config_name='default',
        blank=False,
        validators=[validate_not_empty_html],
    )
    additional_education = CKEditor5Field(
        verbose_name='Дополнительное образование',
        config_name='default',
        blank=True,
    )
    trainings = CKEditor5Field(
        verbose_name='Дополнительное образование',
        config_name='default',
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['order', 'name']

    def _clean_empty_html(self, raw_html):
        text = strip_tags(raw_html or '')
        text = html.unescape(text)
        return '' if not text.strip() else raw_html

    def save(self, *args, **kwargs):
        for fld in ('additional_education', 'trainings'):
            orig = getattr(self, fld)
            setattr(self, fld, self._clean_empty_html(orig))
        super().save(*args, **kwargs)


class TypeDocument(models.Model):
    """Модель для хранения типов документов."""

    name = models.CharField(
        max_length=255, verbose_name='Название типа документа'
    )

    def __str__(self):
        return self.name


class Document(models.Model):
    """Модель для хранения документов."""

    name = models.CharField(max_length=255, verbose_name='Название документа')
    file = models.FileField(
        upload_to=upload_file,
        verbose_name='Файл документа',
    )
    type = models.ForeignKey(
        TypeDocument,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='Тип документа',
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='Сотрудник',
    )
    on_main_page = models.BooleanField(
        default=False, verbose_name='Отображать на главной странице'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
