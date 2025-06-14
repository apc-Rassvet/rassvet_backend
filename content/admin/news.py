"""Модуль настройки административного интерфейса для новостей."""

from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from content.models import Direction, GalleryImage, News, Project


class ProjectFilter(SimpleListFilter):
    """Кастомный фильтр для проектов в административном интерфейсе новостей.

    Обеспечивает сортировку списка проектов по алфавиту в фильтре.
    """

    title = 'проект'
    parameter_name = 'project'

    def lookups(self, request, model_admin):
        """Возвращает список вариантов для фильтра."""
        projects = Project.objects.all().order_by('title')
        return [(project.pk, project.title) for project in projects]

    def queryset(self, request, queryset):
        """Фильтрует queryset на основе выбранного значения."""
        if self.value():
            return queryset.filter(project=self.value())
        return queryset


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
    list_filter = ('date', 'show_on_main', ProjectFilter, 'detail_page_type')
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
