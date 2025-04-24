from django.contrib import admin

from content.models.report import Report, Chapter


class ReportInline(admin.StackedInline):
    model = Report
    extra = 0


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'position', 'count')
    inlines = [ReportInline]

    def count(self, obj):
        return obj.reports.count()

    count.short_description = 'Количество документов'
