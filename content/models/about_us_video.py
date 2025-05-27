"""Модуль about_us_video содержит модель для данных о видео в разделе 'О нас'.

Модели:
    AboutUsVideo: Модель для хранения заголовка и URL ссылки на видео, а также
                  даты создания и обновления.
"""

from django.db import models

from content.mixins import TimestampMixin, TitleMixin


class AboutUsVideo(TimestampMixin, TitleMixin, models.Model):
    """Модель для хранения информации о видео в разделе 'О нас'."""

    url = models.URLField('Ссылка на видео')

    class Meta:
        """Класс Meta, который содержит мета-данные для модели."""

        verbose_name = 'Видео о нас'
        verbose_name_plural = 'Видео о нас'

    def __str__(self):
        """Возвращает строковое представление объекта видео."""
        return self.title

    @classmethod
    def get_solo(cls):
        """Получает единственное видео для раздела 'О нас'.

        Если видео не существует, будет создано одно видео.
        """
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
