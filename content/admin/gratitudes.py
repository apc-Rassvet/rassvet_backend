from django.contrib import admin

from content.models.gratitudes import Gratitude


@admin.register(Gratitude)
class GratitudeAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (
            'Основные данные',
            {'fields': ('title', 'file', 'order', 'is_active')},
        ),
        (
            'Системная информация',
            {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)},
        ),
    )
