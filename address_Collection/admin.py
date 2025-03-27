from django.contrib import admin

from .models import AddressCollection, CollectionPhoto, CollectionTextBlock


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
