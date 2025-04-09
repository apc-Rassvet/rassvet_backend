from django.db import models
from django.utils.translation import gettext_lazy as _


class Mission(models.Model):
    """Модель Миссия страницы "Миссия"."""

    mission_text = models.TextField(
        _('Миссия организации'),
        help_text=_('Основная миссия вашей компании')
    )
    ambitions_text = models.TextField(
        _('Амбиции'),
        help_text=_('Стратегические амбиции и устремления')
    )
    five_year_goal = models.TextField(
        _('Цель на 5 лет'),
        help_text=_('Ключевые цели на 5-летний период')
    )
    tasks_text = models.TextField(
        _('Задачи'),
        help_text=_('Конкретные задачи для достижения целей')
    )
    updated_at = models.DateTimeField(
        _('Последнее обновление'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('Миссия')
        verbose_name_plural = _('Миссия')

    def __str__(self):
        return _('Тексты миссии организации')

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)
