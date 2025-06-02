"""Конфигурация админки для модели Partner.

Этот модуль содержит класс PartnersAdmin,
настраивающий отображение и поведение записей партнеров в админке.
"""

from django.contrib import admin
from django.utils.html import format_html
from ordered_model.admin import OrderedModelAdmin

from content.models import Partner


@admin.register(Partner)
class PartnersAdmin(OrderedModelAdmin):
    """Настройка отображения списка Partner с предпросмотром логотипа."""

    list_display = ('name', 'logo_preview', 'move_up_down_links')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'logo_preview')
    fieldsets = (
        (
            'Основная информация',
            {'fields': ('name', 'logo', 'description')},
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

    @admin.display(description='Логотип')
    def logo_preview(self, obj):
        """Отображает превью логотипа."""
        if obj.logo:
            return format_html('<img src="{}" width="50" />', obj.logo.url)
        return '—'
