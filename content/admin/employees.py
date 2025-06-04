"""Административная конфигурация для моделей Document и Employee.

Этот модуль содержит:
- TypeDocumentInline: настройка отображения типов документов в админке.
- DocumentInline: inline-класс для связанных документов.
- EmployeeAdmin: конфигурация админки для модели Employee.
"""

from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from content.models import Document, Employee, TypeDocument


@admin.register(TypeDocument)
class TypeDocumentInline(admin.ModelAdmin):
    """Настройка отображения модели TypeDocument в админке."""

    fields = ('name',)

    def get_model_perms(self, request):
        """Отключает отображение модели в основном меню админки."""
        return {}


class DocumentInline(admin.TabularInline):
    """Inline-класс для связанных с Employee документов."""

    model = Document
    extra = 1
    validate_min = False
    verbose_name = 'Документ'
    verbose_name_plural = 'Документы'


@admin.register(Employee)
class EmployeeAdmin(OrderedModelAdmin):
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

    def save_model(self, request, obj, form, change):
        """Сохраняет объект модели в админке.

        При создании нового объекта автоматически перемещает его
        на верхнюю позицию (в начало списка), чтобы новые элементы
        отображались первыми. Для уже существующих объектов сохраняет
        стандартное поведение.
        """
        super().save_model(request, obj, form, change)
        if not change:
            obj.top()
            obj.save()
