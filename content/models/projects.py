"""Модуль содержит модели, связанные с Проектами.

Классы:
    ProjectsStatus: Перечисление возможных статусов для Проекта.
Модели:
    1. ProgramsProjects: Модель для хранения информации о программе проекта
    2. ProjectPhoto: Модель для хранения фотографий проекта
    3. Project: Модель для хранения информации о проекте
"""

from django.db import models

from content.mixins import OrderMixin, TitleMixin

from .partners import Partner


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

    status = models.CharField(
        max_length=max(len(value) for value, _ in ProjectsStatus.choices),
        choices=ProjectsStatus.choices,
        default=ProjectsStatus.ACTIVE,
        verbose_name='Статус сбора',
    )
    project_start = models.DateField(
        'Дата старта',
        blank=True,
        null=True,
        default=None,
    )
    project_end = models.DateField(
        'Дата окончания',
        blank=True,
        null=True,
        default=None,
    )
    source_financing = models.ForeignKey(
        Partner,
        on_delete=models.SET_NULL,
        null=True,
        related_name='project',
        verbose_name='Источник софинансирования - Партнёр',
    )
    project_rassvet = models.BooleanField('Проект НКО Рассвет', default=True)
    program = models.ForeignKey(
        ProgramsProjects,
        on_delete=models.SET_NULL,
        null=True,
        related_name='project',
        verbose_name='Проект',
    )
    project_goal = models.TextField(
        verbose_name='Цель проекта', help_text='Введи Цель проекта'
    )
    project_tasks = models.TextField(
        verbose_name='Задачи проекта', help_text='Введи Задачи проекта'
    )
    project_description = models.TextField(
        verbose_name='Описание проекта', help_text='Введи Описание проекта'
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
