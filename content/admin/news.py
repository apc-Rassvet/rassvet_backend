"""Модуль настройки административного интерфейса для новостей."""

from django.contrib import admin
from content.models import News, Direction, GalleryImage


class GalleryImageInline(admin.TabularInline):
    """Инлайн для изображений галереи новости (до 15 штук)."""

    model = GalleryImage
    extra = 1
    max_num = 15


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Настройка административного интерфейса для модели News."""

    inlines = [GalleryImageInline]
    list_display = ('title', 'date', 'show_on_main', 'project')
    list_editable = ('date', 'show_on_main')
    list_filter = ('date', 'show_on_main', 'project', 'detail_page_type')
    search_fields = ('title', 'summary', 'full_text')
    filter_horizontal = ('directions',)
    fieldsets = (
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
        ('Сортировка', {'fields': ('date',)}),
    )


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    """Настройка административного интерфейса для модели Direction."""

    list_display = ('id', 'name')
    search_fields = ('name',)
