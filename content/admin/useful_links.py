"""Административная конфигурация для Полезные ссылки.

Этот модуль содержит:
- ArticleUsefulLinksInline: Inline-класс для статьи Полезные ссылки.
- ChapterUsefulLinksAdmin: Админ зона разделов Полезные ссылки.
"""

from django.contrib import admin

from content.models import ArticleUsefulLinks, ChapterUsefulLinks


class ArticleUsefulLinksInline(admin.StackedInline):
    """Inline-класс для статьи Полезные ссылки."""

    model = ArticleUsefulLinks
    min_num = 1
    show_change_link = True


@admin.register(ChapterUsefulLinks)
class ChapterUsefulLinksAdmin(admin.ModelAdmin):
    """Админ зона разделов Полезные ссылки."""

    list_display = ('title',)
    search_fields = ('title',)
    inlines = (ArticleUsefulLinksInline,)

    def get_queryset(self, request):
        """Возвращает queryset с предзагруженными зависимостями."""
        q_set = super().get_queryset(request)
        return q_set.prefetch_related('article_useful_links')
