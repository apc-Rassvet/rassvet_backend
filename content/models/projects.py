from django.db import models

from content.constants import (
    LENGTH_PROJS_TITLE,
    LENGTH_PROGS_PROJS_TITLE,
    LENGTH_PROJS_STATUS,
)


class ProjectsStatus(models.TextChoices):
    """Статусы проекта."""

    ACTIVE = 'active', 'Действующий'
    COMPLETED = 'completed', 'Завершенный'


class ProgramsProjects(models.Model):
    """Модель программ проектов."""

    title = models.CharField(
        max_length=LENGTH_PROGS_PROJS_TITLE, verbose_name='Заголовок'
    )

    class Meta:
        verbose_name = 'Программа'
        verbose_name_plural = 'Программы'

    def __str__(self):
        return self.title


class Project(models.Model):
    """Модель Проекта."""

    title = models.CharField(
        max_length=LENGTH_PROJS_TITLE, verbose_name='Заголовок'
    )
    logo = models.ImageField(
        upload_to='projects/',
        verbose_name='Логотип',
        blank=False,
        null=False,
    )
    status = models.CharField(
        max_length=LENGTH_PROJS_STATUS,
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
        on_delete=models.CASCADE,
        related_name='project',
        verbose_name='Проект',
    )
    project_goal = models.TextField(verbose_name='Цель проекта')
    project_tasks = models.TextField(verbose_name='Задачи проекта')
    project_description = models.TextField(verbose_name='Описание проекта')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['project_start']

    def __str__(self):
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
        verbose_name = 'Фотография проекта'
        verbose_name_plural = 'Фотографии проектов'

    def __str__(self):
        return f'Фотография для проекта {self.project.title}'
