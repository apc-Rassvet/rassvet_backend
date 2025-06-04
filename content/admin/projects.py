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

    def save_model(self, request, obj, form, change):
        """Сохраняет объект модели в админке.

        При создании нового объекта автоматически перемещает его
        на верхнюю позицию (в начало списка), чтобы новые элементы
        отображались первыми. Для уже существующих объектов сохраняет
        стандартное поведение.
        """
        super().save_model(request, obj, form, change)
        if change is False:
            obj.top()
            obj.save()

    @admin.display(description='Логотип')
    def logo_preview(self, obj):
        """Отображает превью логотипа."""
        if obj.logo:
            return format_html('<img src="{}" width="50" />', obj.logo.url)
        return '—'
