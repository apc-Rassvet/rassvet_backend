from django.contrib import admin
from ..models.review import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'created_at', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'content', 'author_name')

    fieldsets = (
        ('Основные данные', {
            'fields': ('title', 'author_name', 'content', 'is_active')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')
