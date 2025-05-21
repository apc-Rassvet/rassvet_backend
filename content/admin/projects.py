"""Административная конфигурация для проектов и их вложенных элементов.

Этот модуль содержит:
- ProgramsProjectsAdmin: конфигурация для модели ProgramsProjects.
- ProjectPhotoAdmin: inline-класс для фотографий проекта.
- ProjectAdmin: конфигурация для модели Project.
"""

from django.contrib import admin
from django.utils.html import format_html
from ordered_model.admin import OrderedModelAdmin

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
class ProjectAdmin(OrderedModelAdmin):
    """Админ зона Проектов."""

    list_display = (
        'move_up_down_links',
        'order',
        'title',
        'logo_preview',
        'status',
        'project_start',
        'project_end',
        'source_financing',
        'project_rassvet',
        'program',
        'project_goal',
        'project_tasks',
        'project_description',
        'achieved_results',
    )
    list_editable = ('status',)
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

    @admin.display(description='Логотип')
    def logo_preview(self, obj):
        """Отображает превью логотипа."""
        if obj.logo:
            return format_html('<img src="{}" width="50" />', obj.logo.url)
        return '—'
