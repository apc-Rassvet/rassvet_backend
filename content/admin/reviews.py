"""Конфигурация админки для модели Review.

Этот модуль содержит класс ReviewAdmin,
настраивающий отображение и поведение записей партнеров в админке.
"""

from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from content.models import Review


@admin.register(Review)
class ReviewAdmin(OrderedModelAdmin):
    """Настройка отображения списка Review и форм редактирования.

    Определяет отображаемые и редактируемые поля, фильтры, поиск и секции.
    """

    list_display = ('author_name', 'is_active', 'move_up_down_links')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'created_at')
    search_fields = ('content', 'author_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (
            'Основные данные',
            {'fields': ('author_name', 'content', 'is_active')},
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
        if change is False:
            obj.top()
            obj.save()
