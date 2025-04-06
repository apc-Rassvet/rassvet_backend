from django.contrib import admin

from ..models.videos import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_active',)
    fieldsets = (
        ('Основная информация', {'fields': ('title', 'url', 'description')}),
        ('Настройки', {'fields': ('is_active', 'created_at', 'updated_at')}),
    )
