from django.db import models
from django.utils.translation import gettext_lazy as _


class Mission(models.Model):
    mission_text = models.TextField(
        _('Миссия организации'),
        help_text=_('Введите текст миссии организации')
    )
    ambitions_text = models.TextField(
        _('Амбиции'),
        help_text=_('Введите текст об амбициях организации')
    )
    five_year_goal = models.TextField(
        _('Цель на 5 лет'),
        help_text=_('Введите цели организации на 5 лет')
    )
    tasks_text = models.TextField(
        _('Задачи'),
        help_text=_('Введите основные задачи организации')
    )
    updated_at = models.DateTimeField(
        _('Дата последнего обновления'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('миссия')
        verbose_name_plural = _('миссия')

    def __str__(self):
        return _('Текст миссии организации')
