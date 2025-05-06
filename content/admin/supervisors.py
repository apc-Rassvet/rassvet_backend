from django.contrib import admin

from content.models.supervisors import Supervisor, Page


class SupervisorInline(admin.StackedInline):
    model = Supervisor
    extra = 0

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [SupervisorInline]