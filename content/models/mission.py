"""Модуль содержит модели, связанные с Миссиями.

Модели:
    1. Mission: Модель для хранения информации о Миссии
"""

from django.db import models

from content.mixins import OrderMixin
from content.utils import ckeditor_function


class Mission(OrderMixin, models.Model):
    """Модель Миссии."""

    organization_mission = ckeditor_function('Миссия организации')
    ambitions = ckeditor_function('Амбиции')
    goal_for_five_years = ckeditor_function('Цель на 5 пять лет')
    tasks = ckeditor_function('Задачи')

    class Meta:
        """Класс Meta для Mission, содержащий мета-данные."""

        verbose_name = 'Миссия'
        verbose_name_plural = 'Миссии'
        ordering = ['order']

    def __str__(self):
        """Возвращает строковое представление Миссии организации."""
        return self.organization_mission

    @classmethod
    def get_solo(cls):
        """Получает единственную Миссию'.

        Если Миссия не существует, будет создана одна Миссия.
        """
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
