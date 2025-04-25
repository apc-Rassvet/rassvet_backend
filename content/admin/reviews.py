from django.contrib import admin

from content.models.reviews import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'order', 'is_active')
    list_editable = ('order', 'is_active',)
    list_filter = ('is_active', 'created_at')
    search_fields = ('content', 'author_name')

    fieldsets = (
        (
            'Основные данные',
            {'fields': ('author_name', 'content', 'order', 'is_active')},
        ),
        (
            'Системная информация',
            {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)},
        ),
    )

    readonly_fields = ('created_at', 'updated_at')
