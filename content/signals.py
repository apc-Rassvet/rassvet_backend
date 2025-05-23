"""Модуль работы с сигналами проложения."""

from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

from content.models.projects import Project


@receiver(post_save, sender=Project)
def order_handler(sender, instance, created, **kwargs):
    """Хендлер увеличивает у объектов поле 'order' на 1."""
    if created:
        sender.objects.filter(order__gte=instance.order).exclude(
            id=instance.id
        ).update(order=F('order') + 1)
