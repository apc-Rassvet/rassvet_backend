from django.contrib import admin
from django.shortcuts import redirect

from content.models.about_us_video import AboutUsVideo


@admin.register(AboutUsVideo)
class AboutUsVideoAdmin(admin.ModelAdmin):
    """Отображение единственного экземпляра Video в админке."""

    list_display = ('title', 'url')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {'fields': ('title', 'url')}),
        (
            'Служебная информация',
            {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)},
        ),
    )

    def has_add_permission(self, request):
        return not AboutUsVideo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = AboutUsVideo.get_solo()
        return redirect(f'./{obj.pk}/change/')
