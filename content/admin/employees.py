"""Административная конфигурация для моделей Document и Employee.

Этот модуль содержит:
- TypeDocumentInline: настройка отображения типов документов в админке.
- DocumentInline: inline-класс для связанных документов.
- EmployeeAdmin: конфигурация админки для модели Employee.
"""

from django.contrib import admin
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from ordered_model.admin import OrderedModelAdmin

from content.mixins import CharCountAdminMixin
from content.models import Document, Employee, TypeDocument


@admin.register(TypeDocument)
class TypeDocumentInline(admin.ModelAdmin):
    """Настройка отображения модели TypeDocument в админке."""

    fields = ('name',)
    search_fields = ('name',)

    def get_model_perms(self, request):
        """Отключает отображение модели в основном меню админки."""
        return {}


class DocumentInline(admin.TabularInline):
    """Inline-класс для связанных с Employee документов."""

    model = Document
    extra = 1
    validate_min = False
    autocomplete_fields = ['type']
    verbose_name = 'Документ'
    verbose_name_plural = 'Дипломы и сертификаты'

    class Media:
        js = (
            'admin/js/jquery.init.js',
            'custom_admin/js/inline_instant_delete.js',
        )

    def get_queryset(self, request):
        """Оптимизация для инлайнов: select_related для ForeignKey (type)."""
        qs = super().get_queryset(request)
        return qs.select_related('type')


@admin.register(Employee)
class EmployeeAdmin(CharCountAdminMixin, OrderedModelAdmin):
    """Конфигурация админки для модели Employee.

    Определяет отображаемые поля, фильтрацию, поиск, inline-классы и fieldsets.
    """

    charcount_fields = {
        'name': 19,
        'main_specialities': 45,
    }
    list_display = ('name', 'category_on_main', 'move_up_down_links')
    list_editable = ('category_on_main',)
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [DocumentInline]
    fieldsets = (
        (
            'Основные данные',
            {
                'fields': (
                    'name',
                    'image',
                    'main_specialities',
                    'trainings',
                    'interviews',
                    'specialists_register',
                    'category_on_main',
                    'specialities',
                    'education',
                    'additional_education',
                )
            },
        ),
        (
            'Системная информация',
            {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)},
        ),
    )

    def get_queryset(self, request):
        """Оптимизация N+1 — prefetch_related для связанных документов."""
        qs = super().get_queryset(request)
        return qs.prefetch_related('documents')

    def get_urls(self):
        """Добавляет URL для удаления записи в inline модели."""
        return [
            path(
                'inline-delete/<int:pk>/',
                self.admin_site.admin_view(self.inline_delete_view),
                name='content_document_inline_delete',
            ),
        ] + super().get_urls()

    @method_decorator(csrf_protect)
    def inline_delete_view(self, request, pk: int):
        """Удаляет запись в inline модели."""
        if request.method != 'POST':
            return HttpResponseForbidden('POST required')

        if not request.user.has_perm('content.delete_document'):
            return HttpResponseForbidden('No permission')

        doc = get_object_or_404(Document, pk=pk)

        employee_pk = request.POST.get('employee_id')
        if employee_pk and str(doc.employee_id) != str(employee_pk):
            raise Http404('Document does not belong to this employee')

        if hasattr(doc, 'file') and getattr(doc.file, 'name', None):
            try:
                doc.file.delete(save=False)
            except Exception:
                pass

        doc.delete()
        return JsonResponse({'ok': True, 'deleted': pk})
