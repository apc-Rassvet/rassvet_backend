from django.contrib import admin
from .models import AddressCollection, CollectionPhoto, CollectionTextBlock, Partner
from django.utils.translation import gettext_lazy as _


class CollectionPhotoInline(admin.TabularInline):
    model = CollectionPhoto
    extra = 0
    max_num = 3


class CollectionTextBlockInline(admin.TabularInline):
    model = CollectionTextBlock
    extra = 0
    max_num = 3


@admin.register(AddressCollection)
class AddressCollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'order', 'created_at')
    list_editable = ('order', 'status')
    list_filter = ('status',)
    inlines = [CollectionPhotoInline, CollectionTextBlockInline]
    actions = ['move_to_active', 'move_to_completed']

    def move_to_active(self, request, queryset):
        queryset.update(status='active')

    move_to_active.short_description = "Переместить в актуальные"

    def move_to_completed(self, request, queryset):
        queryset.update(status='completed')

    move_to_completed.short_description = "Переместить в завершенные"


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_preview', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('logo_preview', 'created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('name', 'logo', 'logo_preview', 'description')
        }),
        (_('Дополнительная информация'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def logo_preview(self, obj):
        from django.utils.html import format_html
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.logo.url)
        return _("Нет логотипа")

    logo_preview.short_description = _('Превью логотипа')

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            return readonly_fields + ('created_at', 'updated_at')
        return readonly_fields