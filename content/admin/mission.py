"""Административная конфигурация для Миссий и их вложенных элементов.

Этот модуль содержит:
- MissionAdmin: конфигурация для модели Mission.
"""

from django.contrib import admin
from django.shortcuts import redirect

from content.models.mission import Mission


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    """Админ зона Миссий."""

    list_display = (
        'order',
        'organization_mission',
        'ambitions',
        'goal_for_five_years',
        'tasks',
    )
    # list_editable = (
    #     'organization_mission',
    #     'ambitions',
    #     'goal_for_five_years',
    #     'tasks',
    # )
    list_filter = ('order',)
    empty_value_display = '-пусто-'

    def has_add_permission(self, request):
        """Разрешает добавление нового объекта, если экземпляр не создан."""
        return not Mission.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Запрещает удаление объекта AboutUsVideo в админке."""
        return False

    def changelist_view(self, request, extra_context=None):
        """Перенаправляет на страницу изменения экземпляра AboutUsVideo."""
        obj = Mission.get_solo()
        return redirect(f'./{obj.pk}/change/')
