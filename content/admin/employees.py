from django.contrib import admin

from content.models import employees as team_models


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
    list_display = ('name', 'order', 'category_on_main')
    list_editable = ('order', 'category_on_main')
    list_filter = ('order',)
    search_fields = ['name',]
    inlines = [
        DocumentInline
    ]
