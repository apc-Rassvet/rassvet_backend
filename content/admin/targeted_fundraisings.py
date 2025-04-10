from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from content.models import targeted_fundraisings as fundraisings_models


class FundraisingPhotoInline(admin.TabularInline):
    model = fundraisings_models.FundraisingPhoto
    extra = 1
    min_num = 1
    max_num = 3
    validate_min = True


class FundraisingTextBlockInline(admin.TabularInline):
    model = fundraisings_models.FundraisingTextBlock
    extra = 1
    min_num = 1
    max_num = 3
    validate_min = True


@admin.register(fundraisings_models.TargetedFundraising)
class TargetedFundraisingAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'order', 'created_at')
    list_editable = ('order', 'status')
    list_filter = ('status',)
    inlines = [FundraisingPhotoInline, FundraisingTextBlockInline]
    actions = ['move_to_active', 'move_to_completed']

    @admin.action(description='Переместить в актуальные')
    def move_to_active(self, request, queryset):
        queryset.update(status='active')

    @admin.action(description='Переместить в завершенные')
    def move_to_completed(self, request, queryset):
        queryset.update(status='completed')
