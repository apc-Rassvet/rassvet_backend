"""Административная конфигурация для проектов и их вложенных элементов.

Этот модуль содержит:
- ProgramsProjectsAdmin: конфигурация для модели ProgramsProjects.
- ProjectPhotoAdmin: inline-класс для фотографий проекта.
- ProjectAdmin: конфигурация для модели Project.
"""

from django.contrib import admin

from content.models.projects import ProgramsProjects, Project, ProjectPhoto


@admin.register(ProgramsProjects)
class ProgramsProjectsAdmin(admin.ModelAdmin):
    """Админ зона Программ."""

    list_display = ('title',)
    search_fields = ('title',)


class ProjectPhotoAdmin(admin.StackedInline):
    """Inline-класс для фотографий, прикреплённых к проекту."""

    model = ProjectPhoto
    min_num = 1
    max_num = 3


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Админ зона Проектов."""

    list_display = (
        'title',
        'status',
        'project_start',
        'project_end',
        'project_rassvet',
        'program',
        'order',
    )
    list_editable = (
        'status',
        'project_end',
        'project_rassvet',
    )
    list_filter = (
        'order',
        'title',
        'status',
    )
    search_fields = (
        'order',
        'title',
        'status',
    )
    inlines = (ProjectPhotoAdmin,)
    empty_value_display = '-пусто-'
