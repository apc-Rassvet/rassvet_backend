"""Административная конфигурация для Миссий и их вложенных элементов.

Этот модуль содержит:
- MissionAdmin: конфигурация для модели Mission.
"""

from django.contrib import admin

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
    list_editable = (
        'organization_mission',
        'ambitions',
        'goal_for_five_years',
        'tasks',
    )
    list_filter = ('order',)
    empty_value_display = '-пусто-'
