from django.db import models

from content.constants import LENGTH_ABOUT_VIDEO_TITLE


class AboutUsVideo(models.Model):
    """Модель для 'Видео' в разделе 'О нас'."""

    title = models.CharField('Заголовок', max_length=LENGTH_ABOUT_VIDEO_TITLE)
    url = models.URLField('Ссылка на видео')
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Видео о нас'
        verbose_name_plural = 'Видео о нас'

    def __str__(self):
        return self.title

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
