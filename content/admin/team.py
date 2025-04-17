from django.contrib import admin

from content.models import team as team_models


class SpecialityInline(admin.TabularInline):
    model = team_models.Speciality
    extra = 3
    min_num = 1
    validate_min = True


class EducationInline(admin.TabularInline):
    model = team_models.Education
    extra = 1
    validate_min = False


class AdditionalEducationInline(admin.TabularInline):
    model = team_models.AdditionalEducation
    extra = 1
    validate_min = False


class TrainingsInline(admin.TabularInline):
    model = team_models.Trainings
    extra = 1
    validate_min = False


class DocumentInline(admin.TabularInline):
    model = team_models.Document
    extra = 1
    validate_min = False


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
