"""Административная конфигурация для отчётов и их вложенных элементов.

Этот модуль содержит:
- ChapterAdmin: конфигурация для модели Chapter.
- ReportInline: inline-класс для отчётов.
"""

from django.contrib import admin

from content.base_models import BaseOrderedModelAdmin
from content.models.training_and_internships import (
    TrainingAndInternships,
    TrainingAndInternshipsPhoto,
)


class TrainingAndInternshipsPhotoInline(admin.TabularInline):
    """Inline-класс для фотографий."""

    model = TrainingAndInternshipsPhoto
    min_num = 1
    max_num = 3


@admin.register(TrainingAndInternships)
class TrainingAndInternshipsAdmin(BaseOrderedModelAdmin):
    """Конфигурация админки для модели TrainingAndInternships."""

    list_display = [
        'title',
        'date',
        'price',
        'move_up_down_links',
    ]
    inlines = [TrainingAndInternshipsPhotoInline]
