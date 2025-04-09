from django.contrib import admin
from django.utils.html import format_html

from ..models.partners import Partner


@admin.register(Partner)
class PartnersAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_preview', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'logo_preview')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'logo', 'description')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Логотип')
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" />', obj.logo.url)
        return '—'
