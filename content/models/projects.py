"""Модуль содержит модели, связанные с Проектами.

Классы:
    ProjectsStatus: Перечисление возможных статусов для Проекта.

Модели:
    1. ProgramsProjects: Модель для хранения информации о программе проекта
    2. ProjectPhoto: Модель для хранения фотографий проекта
    3. Project: Модель для хранения информации о проекте
"""

from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from content.mixins import OrderMixin, TitleMixin
from content.validators import validate_not_empty_html


class ProjectsStatus(models.TextChoices):
    """Статусы проекта."""

    ACTIVE = 'active', 'Действующий'
    COMPLETED = 'completed', 'Завершенный'


class ProgramsProjects(TitleMixin, models.Model):
    """Модель программ проектов."""

    class Meta:
        """Класс Meta для ProgramsProjects, содержащий мета-данные."""

        verbose_name = 'Программа'
        verbose_name_plural = 'Программы'

    def __str__(self):
        """Возвращает строковое представление программы."""
        return self.title


class Project(OrderMixin, TitleMixin, models.Model):
    """Модель Проекта."""

    logo = models.ImageField(
        upload_to='projects/',
        verbose_name='Логотип',
        blank=False,
        null=False,
    )
    status = models.CharField(
        max_length=max(len(value) for value, _ in ProjectsStatus.choices),
        choices=ProjectsStatus.choices,
        default=ProjectsStatus.ACTIVE,
        verbose_name='Статус сбора',
    )
    project_start = models.DateTimeField('Дата старта', auto_now_add=True)
    project_end = models.DateTimeField(
        'Дата окончания',
        blank=True,
        null=True,
    )
    source_financing = models.TextField(
        verbose_name='Источник софинансирования'
    )
    project_rassvet = models.BooleanField('Проект НКО Рассвет', default=True)
    program = models.ForeignKey(
        ProgramsProjects,
        on_delete=models.SET_NULL,
        null=True,
        related_name='project',
        verbose_name='Проект',
    )
    project_goal = CKEditor5Field(
        verbose_name='Цель проекта',
        config_name='default',
        blank=False,
        validators=[validate_not_empty_html],
    )
    project_tasks = CKEditor5Field(
        verbose_name='Задачи проекта',
        config_name='default',
        blank=False,
        validators=[validate_not_empty_html],
    )
    project_description = CKEditor5Field(
        verbose_name='Описание проекта',
        config_name='default',
        blank=False,
        validators=[validate_not_empty_html],
    )

    class Meta:
        """Класс Meta для Project, содержащий мета-данные."""

        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['order', '-project_start']

    def __str__(self):
        """Возвращает строковое представление проекта."""
        return self.title


class ProjectPhoto(models.Model):
    """Модель Фотографий проекта."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='photo',
        verbose_name='Проект',
    )
    image = models.ImageField(
        upload_to='projects/',
        verbose_name='Фотография',
        blank=False,
        null=False,
    )

    class Meta:
        """Класс Meta для ProjectPhoto, содержащий мета-данные."""

        verbose_name = 'Фотография проекта'
        verbose_name_plural = 'Фотографии проектов'

    def __str__(self):
        """Возвращает строковое представление проекта фотографии."""
        return f'Фотография для проекта {self.project.title}'
