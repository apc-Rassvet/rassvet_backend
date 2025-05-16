"""Конфигурация админки для модели Partner.

Этот модуль содержит класс PartnersAdmin,
настраивающий отображение и поведение записей партнеров в админке.
"""

from django.contrib import admin
from django.utils.html import format_html

from content.models import Partner


@admin.register(Partner)
class PartnersAdmin(admin.ModelAdmin):
    """Настройка отображения списка Partner с предпросмотром логотипа.

    Определяет поля для списка, фильтры, поиск, readonly-поля
    и секции полей для редактирования.
    """

    list_display = ('name', 'logo_preview', 'order')
    list_editable = ('order',)
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'logo_preview')
    fieldsets = (
        (
            'Основная информация',
            {'fields': ('name', 'logo', 'description', 'order')},
        ),
        (
            'Системная информация',
            {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)},
        ),
    )

    @admin.display(description='Логотип')
    def logo_preview(self, obj):
        """Отображает превью логотипа."""
        if obj.logo:
            return format_html('<img src="{}" width="50" />', obj.logo.url)
        return '—'
