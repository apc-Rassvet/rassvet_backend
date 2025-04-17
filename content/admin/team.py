from django.contrib import admin

from content.models import Document, Employee, TypeDocument


@admin.register(TypeDocument)
class TypeDocumentAdmin(admin.ModelAdmin):
    list_display = ('type',)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'team_member')


@admin.register(Employee)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'telephone', 'image')
