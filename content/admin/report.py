"""Административная конфигурация для отчётов и их вложенных элементов.

Этот модуль содержит:
- ChapterAdmin: конфигурация для модели Chapter.
- ReportInline: inline-класс для отчётов.
"""

from django.contrib import admin

from content.models.report import Report, Chapter


class ReportInline(admin.StackedInline):
    """Модель администрирования документов."""

    model = Report
    extra = 0


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    """Модель администрирования разделов отчетов."""

    list_display = ('title', 'position', 'count')
    inlines = [ReportInline]

    @admin.display(description='Количество документов')
    def count(self, obj):
        """Возвращает количество отчётов."""
        return obj.reports.count()
