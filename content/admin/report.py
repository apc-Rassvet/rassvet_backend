"""Административная конфигурация для отчётов и их вложенных элементов.

Этот модуль содержит:
- ChapterAdmin: конфигурация для модели Chapter.
- ReportInline: inline-класс для отчётов.
"""

from django.contrib import admin

from ordered_model.admin import (
    OrderedModelAdmin,
    OrderedTabularInline,
    OrderedInlineModelAdminMixin,
)

from content.models.report import Report, Chapter


class ReportInline(OrderedTabularInline):
    """Модель администрирования документов."""

    model = Report
    fields = (
        'title',
        'file',
        'download_icon',
        'move_up_down_links',
    )
    readonly_fields = ('move_up_down_links',)
    ordering = ('order',)
    extra = 1


@admin.register(Chapter)
class ChapterAdmin(OrderedInlineModelAdminMixin, OrderedModelAdmin):
    """Модель администрирования разделов отчетов."""

    list_display = ('title', 'count', 'move_up_down_links')
    inlines = [ReportInline]
    search_fields = ('title',)

    @admin.display(description='Количество документов')
    def count(self, obj):
        """Возвращает количество отчётов."""
        return obj.reports.count()
