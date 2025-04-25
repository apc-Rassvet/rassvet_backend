from django.contrib import admin
from django.core.exceptions import ValidationError

from content.models import targeted_fundraisings as fundraisings_models


def validate_forms(forms, error_detail):
    cleaned_forms = [
        form
        for form in forms
        if form.cleaned_data and not form.cleaned_data.get('DELETE', False)
    ]
    if len(cleaned_forms) < 1:
        raise ValidationError(error_detail)


class BaseValidatedInline(admin.TabularInline):
    extra = 0
    min_num = 1
    max_num = 3
    validate_min = True
    validation_error_message = 'Необходим минимум один элемент'

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        error_message = self.validation_error_message
        original_clean = formset.clean

        def custom_clean(self):
            original_clean(self)
            validate_forms(self.forms, error_message)

        formset.clean = custom_clean
        return formset


class FundraisingPhotoInline(BaseValidatedInline):
    model = fundraisings_models.FundraisingPhoto
    validation_error_message = 'Должна быть как минимум одна фотография.'


class FundraisingTextBlockInline(BaseValidatedInline):
    model = fundraisings_models.FundraisingTextBlock
    validation_error_message = 'Должен быть как минимум один текстовый блок.'


@admin.register(fundraisings_models.TargetedFundraising)
class TargetedFundraisingAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'fundraising_link', 'order')
    list_editable = ('order', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('title',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [FundraisingPhotoInline, FundraisingTextBlockInline]
    actions = ['move_to_active', 'move_to_completed']

    fieldsets = (
        (
            'Основные данные',
            {
                'fields': (
                    'title',
                    'short_description',
                    'fundraising_link',
                    'status',
                    'order',
                )
            },
        ),
        (
            'Системная информация',
            {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)},
        ),
    )

    @admin.action(description='Переместить в актуальные')
    def move_to_active(self, request, queryset):
        queryset.update(status='active')

    @admin.action(description='Переместить в завершенные')
    def move_to_completed(self, request, queryset):
        queryset.update(status='completed')
