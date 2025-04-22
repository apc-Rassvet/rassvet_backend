from django import forms
from django.urls import path
from django.contrib import admin
from django.utils.functional import cached_property
from django.template.loader import get_template
from content.models import team as team_models
from nested_inline.admin import NestedStackedInline, NestedModelAdmin


class SpecialityInline(admin.TabularInline):
    model = team_models.Speciality
    extra = 3
    min_num = 1
    max_num = 3
    validate_min = True
    verbose_name = 'Специальность'
    verbose_name_plural = 'Специальности'


class EducationInline(admin.TabularInline):
    model = team_models.Education
    extra = 1
    min_num = 1
    max_num = 3
    validate_min = False
    verbose_name = 'Образование'
    verbose_name_plural = 'Образование'


class AdditionalEducationInline(admin.TabularInline):
    model = team_models.AdditionalEducation
    extra = 1
    max_num = 5
    validate_min = False
    verbose_name = 'Дополнительное образование'
    verbose_name_plural = 'Дополнительное образование'


class TrainingsInline(admin.TabularInline):
    model = team_models.Trainings
    extra = 1
    validate_min = False
    verbose_name = 'Тренинги'
    verbose_name_plural = 'Тренинги'


@admin.register(team_models.TypeDocument)
class TypeDocument(admin.ModelAdmin):
    fields = ('name',)

    def get_model_perms(self, request):
        return {}


class DocumentInline(admin.TabularInline):
    model = team_models.Document
    extra = 1
    validate_min = False
    verbose_name = 'Документ'
    verbose_name_plural = 'Документы'


@admin.register(team_models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'ordaring', 'category_on_main')
    search_fields = ['name',]
    list_filter = ('ordaring',)
    inlines = [
        SpecialityInline,
        EducationInline,
        AdditionalEducationInline,
        TrainingsInline,
        DocumentInline
    ]
