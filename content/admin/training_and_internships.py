"""Административная конфигурация для отчётов и их вложенных элементов.

Этот модуль содержит:
- ChapterAdmin: конфигурация для модели Chapter.
- ReportInline: inline-класс для отчётов.
"""

from django.contrib import admin

from content.models.training_and_internships import (
    TrainingAndInternships,
    TAIPhoto,
)


class TAIPhotoInline(admin.TabularInline):
    """Inline-класс для фотографий."""

    model = TAIPhoto
    extra = 3


@admin.register(TrainingAndInternships)
class TrainingAndInternshipsAdmin(admin.ModelAdmin):
    """Конфигурация админки для модели TrainingAndInternships."""

    list_display = ['title', 'date', 'price']
    inlines = [TAIPhotoInline]
