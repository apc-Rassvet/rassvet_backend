"""Модуль содержит модели, связанные с Миссиями.

Модели:
    1. Mission: Модель для хранения информации о Миссии
"""

from django.db import models

from content.mixins import OrderMixin


class Mission(OrderMixin, models.Model):
    """Модель Миссии."""

    organization_mission = models.TextField(
        verbose_name='Миссия организации',
        help_text='Добавте Миссию организации',
    )
    ambitions = models.TextField(
        verbose_name='Амбиции',
        help_text='Добавте Амбиции',
    )
    goal_for_five_years = models.TextField(
        verbose_name='Цель на 5 пять лет',
        help_text='Добавте Цель на 5 пять лет',
    )
    tasks = models.TextField(
        verbose_name='Задачи',
        help_text='Добавте Задачу',
    )

    class Meta:
        """Класс Meta для Mission, содержащий мета-данные."""

        verbose_name = 'Миссия'
        verbose_name_plural = 'Миссии'
        ordering = ['order']

    def __str__(self):
        """Возвращает строковое представление Миссии организации."""
        return self.organization_mission
