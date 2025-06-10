"""Модуль настройки административного интерфейса для новостей."""

from django.contrib import admin
from ordered_model.admin import (
    OrderedTabularInline,
    OrderedInlineModelAdminMixin,
)
from content.models import News, Direction, GalleryImage


class GalleryImageInline(OrderedTabularInline):
    """Инлайн для изображений галереи новости (до 15 штук)."""

    model = GalleryImage
    fields = (
        'image',
        'name',
        'move_up_down_links',
    )
    readonly_fields = ('move_up_down_links',)
    ordering = ('order',)
    extra = 1
    max_num = 15


@admin.register(News)
class NewsAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    """Настройка административного интерфейса для модели News."""

    inlines = [GalleryImageInline]
    list_display = ('title', 'date', 'show_on_main', 'project')
    list_editable = ('date', 'show_on_main')
    list_filter = ('date', 'show_on_main', 'project', 'detail_page_type')
    search_fields = ('title', 'summary', 'full_text')
    filter_horizontal = ('directions',)
    fieldsets = (
        ('Сортировка', {'fields': ('date',)}),
        (
            None,
            {
                'fields': (
                    'title',
                    'photo',
                    'course_start',
                    'summary',
                    'directions',
                    'project',
                )
            },
        ),
        (
            'Детализация',
            {
                'fields': (
                    'detail_page_type',
                    'detail_page_link',
                    'show_on_main',
                )
            },
        ),
        (
            'Контент подробной страницы',
            {
                'fields': (
                    'full_text',
                    'video_url',
                )
            },
        ),
    )


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    """Настройка административного интерфейса для модели Direction."""

    list_display = ('id', 'name')
    search_fields = ('name',)
