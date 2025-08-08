"""Административная конфигурация для моделей Document и Employee.

Этот модуль содержит:
- TypeDocumentInline: настройка отображения типов документов в админке.
- DocumentInline: inline-класс для связанных документов.
- EmployeeAdmin: конфигурация админки для модели Employee.
"""

from django.contrib import admin

from content.base_models import BaseOrderedModelAdmin
from content.models import Document, Employee, TypeDocument


@admin.register(TypeDocument)
class TypeDocumentInline(admin.ModelAdmin):
    """Настройка отображения модели TypeDocument в админке."""

    fields = ('name',)
    search_fields = ('name',)

    def get_model_perms(self, request):
        """Отключает отображение модели в основном меню админки."""
        return {}


class DocumentInline(admin.TabularInline):
    """Inline-класс для связанных с Employee документов."""

    model = Document
    extra = 1
    validate_min = False
    autocomplete_fields = ['type']
    verbose_name = 'Документ'
    verbose_name_plural = 'Документы'

    def get_queryset(self, request):
        """Оптимизация для инлайнов: select_related для ForeignKey (type)."""
        qs = super().get_queryset(request)
        return qs.select_related('type')


@admin.register(Employee)
class EmployeeAdmin(BaseOrderedModelAdmin):
    """Конфигурация админки для модели Employee.

    Определяет отображаемые поля, фильтрацию, поиск, inline-классы и fieldsets.
    """

    list_display = ('name', 'category_on_main', 'move_up_down_links')
    list_editable = ('category_on_main',)
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [DocumentInline]
    fieldsets = (
        (
            'Основные данные',
            {
                'fields': (
                    'name',
                    'image',
                    'main_specialities',
                    'interviews',
                    'specialists_register',
                    'category_on_main',
                    'specialities',
                    'education',
                    'additional_education',
                    'trainings',
                )
            },
        ),
        (
            'Системная информация',
            {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)},
        ),
    )

    def get_queryset(self, request):
        """Оптимизация N+1 — prefetch_related для связанных документов."""
        qs = super().get_queryset(request)
        return qs.prefetch_related('documents')
