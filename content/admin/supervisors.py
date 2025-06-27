from django.contrib import admin

from content.base_models import BaseOrderedModelAdmin
from content.models.supervisors import Supervisor


@admin.register(Supervisor)
class SupervisorAdmin(BaseOrderedModelAdmin):
    """Модель администрирования супервизоров."""

    list_display = ('name', 'position', 'move_up_down_links')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('directions',)
    filter_horizontal = ('directions',)
