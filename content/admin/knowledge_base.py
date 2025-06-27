"""Административная конфигурация для Базы Знаний.

Этот модуль содержит:
- ArticleGallerykAdmin: Inline-класс для Галерея фото.
- ArticleTextBlockAdmin: Inline-класс для Текстовый блок.
- ChapterKnowledgeBaseAdmin: Админ зона разделов Базы знаний.
- ArticleAdmin: Админ зона статьи Базы знаний.
"""

from django.contrib import admin

from content.models import (
    Article,
    ArticleGallery,
    ArticleTextBlock,
    ChapterKnowledgeBase,
)


@admin.register(ChapterKnowledgeBase)
class ChapterKnowledgeBaseAdmin(admin.ModelAdmin):
    """Админ зона разделов Базы знаний."""

    list_display = ('title',)
    search_fields = ('title',)


class ArticleGallerykAdmin(admin.StackedInline):
    """Inline-класс для Галерея фото статьи Базы знаний."""

    model = ArticleGallery
    min_num = 0
    max_num = 15


class ArticleTextBlockAdmin(admin.StackedInline):
    """Inline-класс для Текстовый блок статьи Базы знаний."""

    model = ArticleTextBlock
    extra = 1
    max_num = 3


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Админ зона статьи Базы знаний."""

    list_display = (
        'title',
        'chapter',
    )
    list_filter = ('chapter',)
    search_fields = ('title',)
    inlines = (ArticleGallerykAdmin, ArticleTextBlockAdmin)
