from django.contrib import admin

from content.models.supervisors import Supervisor


@admin.register(Supervisor)
class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'page')
    list_filter = ('page',)
