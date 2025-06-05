"""Административная конфигурация для проектов и их вложенных элементов.

Этот модуль содержит:
- ProgramsProjectsAdmin: конфигурация для модели ProgramsProjects.
- ProjectPhotoAdmin: inline-класс для фотографий проекта.
- ProjectAdmin: конфигурация для модели Project.
"""

from django.contrib import admin
from django.utils.html import format_html

from content.base_models import BaseOrderedModelAdmin
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
class ProjectAdmin(BaseOrderedModelAdmin):
    """Админ зона Проектов."""

    list_display = (
        'title',
        'status',
        'logo_preview',
        'move_up_down_links',
    )
    list_editable = ('status',)
    list_filter = (
        'title',
        'status',
    )
    search_fields = (
        'title',
        'status',
    )
    inlines = (ProjectPhotoAdmin,)
    empty_value_display = '-пусто-'

    @admin.display(description='Логотип')
    def logo_preview(self, obj):
        """Отображает превью логотипа."""
        if obj.logo:
            return format_html('<img src="{}" width="50" />', obj.logo.url)
        return '—'
