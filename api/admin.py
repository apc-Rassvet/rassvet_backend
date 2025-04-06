from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Mission


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Миссия организации'), {
            'fields': ('mission_text',)
        }),
        (_('Амбиции'), {
            'fields': ('ambitions_text',)
        }),
        (_('Цели'), {
            'fields': ('five_year_goal',)
        }),
        (_('Задачи'), {
            'fields': ('tasks_text',)
        }),
        (_('Метаданные'), {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('updated_at',)
    list_display = ('__str__', 'updated_at')

    def has_add_permission(self, request):
        return not Mission.objects.exists()
