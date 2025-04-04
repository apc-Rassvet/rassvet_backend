from django.contrib import admin

from .models import Document, Team, TypeDocument

class TypeDocumentAdmin(admin.ModelAdmin):
    list_display = ('type',)

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'team_member')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'telephone', 'image')

admin.site.register(TypeDocument)
admin.site.register(Document)
admin.site.register(Team)
