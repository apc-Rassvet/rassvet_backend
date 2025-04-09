from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from ..models.mission import Mission


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Основной контент'), {
            'fields': (
                'mission_text',
                'ambitions_text',
                'five_year_goal',
                'tasks_text'
            )
        }),
        (_('Мета-информация'), {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('updated_at',)
    list_display = ('updated_at',)

    def has_add_permission(self, request):
        """Разрешаем создание только если нет записей"""
        return not Mission.objects.exists()
