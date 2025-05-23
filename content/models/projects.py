"""Модуль содержит модели, связанные с Проектами.

Классы:
    ProjectsStatus: Перечисление возможных статусов для Проекта.
Модели:
    1. ProgramsProjects: Модель для хранения информации о программе проекта
    2. ProjectPhoto: Модель для хранения фотографий проекта
    3. Project: Модель для хранения информации о проекте
"""

from django.db import models
from django.db.models import CheckConstraint, F, Q
from ordered_model.models import OrderedModel

from content.mixins import OrderMixin, TitleMixin
from content.utils import ckeditor_function

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


class Project(OrderMixin, TitleMixin, OrderedModel):
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
        blank=True,
        null=True,
        related_name='project',
        verbose_name='Источник софинансирования - Партнёр',
    )
    project_rassvet = models.BooleanField('Проект НКО Рассвет', default=False)
    program = models.ForeignKey(
        ProgramsProjects,
        on_delete=models.SET_NULL,
        null=True,
        related_name='project',
        verbose_name='Программа',
    )
    project_goal = ckeditor_function(verbose_name='Цель проекта')
    project_tasks = ckeditor_function(verbose_name='Задачи проекта')
    project_description = ckeditor_function(verbose_name='Описание проекта')
    achieved_results = ckeditor_function(
        verbose_name='Достигнутые результаты',
        blank=True,
        null=True,
        validators=[],
    )
    order_field_name = 'order'

    class Meta:
        """Класс Meta для Project, содержащий мета-данные."""

        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['order']
        constraints = [
            CheckConstraint(
                check=Q(project_end__gt=F('project_start')),
                name='Дата старта не может быть позже даты окончания проекта',
            ),
        ]

    def __str__(self):
        """Возвращает строковое представление проекта."""
        return self.title

    def save(self, *args, **kwargs):
        """Переопределяет метод сохранения для очистки HTML-контента в полях.

        Этот метод проверяет поле achieved_results на наличие
        пустого HTML-контента и присваивает None.
        """
        if self.achieved_results == '<p>&nbsp;</p>':
            self.achieved_results = None
        super().save(*args, **kwargs)


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
