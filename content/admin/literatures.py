from django.contrib import admin

from content.base_models import BaseOrderedModelAdmin
from content.models import Literature


@admin.register(Literature)
class LiteratureAdmin(BaseOrderedModelAdmin):
    """Модель администрирования литературы."""

    list_display = (
        'title',
        'author',
        'publication_year',
        'move_up_down_links',
    )
    search_fields = ('title', 'author')
