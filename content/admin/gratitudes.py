from django.contrib import admin

from ..models.gratitudes import Gratitude


@admin.register(Gratitude)
class GratitudeAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at',)
    list_editable = ('order', 'is_active')
    fieldsets = (
        ('Основная информация', {'fields': ('title', 'content', 'file')}),
        (
            'Настройки отображения',
            {'fields': ('order', 'is_active', 'created_at')},
        ),
    )
