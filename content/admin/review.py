from django.contrib import admin

from .form import ReviewForm
from ..models.review import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    form = ReviewForm
    list_display = ('title', 'author', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'is_active')
        }),
        ('Системная информация', {
            'fields': ('author', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)
