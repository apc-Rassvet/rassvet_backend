"""Модуль настройки административного интерфейса для новостей."""

from django.contrib import admin
from content.models import News, Direction, GalleryImage


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Настройка административного интерфейса для модели News."""

    list_display = ('id', 'title', 'date', 'show_on_main')
    list_filter = ('date', 'show_on_main', 'detail_page_type')
    search_fields = ('title', 'summary', 'full_text')
    filter_horizontal = ('directions', 'additional_images')
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'title',
                    'photo',
                    'date',
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
                    'gallery',
                    'additional_images',
                    'video_url',
                    'video_format',
                )
            },
        ),
        ('Сортировка', {'fields': ('order',)}),
    )


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    """Настройка административного интерфейса для модели Direction."""

    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    """Настройка административного интерфейса для модели GalleryImage."""

    list_display = ('id', 'image')
