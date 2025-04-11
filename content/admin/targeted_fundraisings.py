from django.contrib import admin
from django.core.exceptions import ValidationError

from content.models import targeted_fundraisings as fundraisings_models


class FundraisingPhotoInline(admin.TabularInline):
    model = fundraisings_models.FundraisingPhoto
    extra = 1
    min_num = 1
    max_num = 3
    validate_min = True

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        def custom_clean(self):
            super(type(self), self).clean()
            count = 0
            for form in self.forms:
                if form.cleaned_data and not form.cleaned_data.get(
                    'DELETE', False
                ):
                    count += 1
            if count < 1:
                raise ValidationError(
                    'Должна быть как минимум одна фотография'
                )

        formset.clean = custom_clean
        return formset


class FundraisingTextBlockInline(admin.TabularInline):
    model = fundraisings_models.FundraisingTextBlock
    extra = 1
    min_num = 1
    max_num = 3
    validate_min = True

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        def custom_clean(self):
            super(type(self), self).clean()
            count = 0
            for form in self.forms:
                if form.cleaned_data and not form.cleaned_data.get(
                    'DELETE', False
                ):
                    count += 1
            if count < 1:
                raise ValidationError(
                    'Должен быть как минимум один текстовый блок'
                )

        formset.clean = custom_clean
        return formset


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
