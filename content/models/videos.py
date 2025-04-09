from django.db import models
from django.core.validators import URLValidator

from ..constants import LENGTH_VIDEO_TITLE


class Video(models.Model):
    """Модель для 'Видео' в разделе 'О нас'."""

    title = models.CharField('Заголовок', max_length=LENGTH_VIDEO_TITLE)
    url = models.URLField('Ссылка на видео', validators=[URLValidator()])
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    is_active = models.BooleanField('Активно', default=True)

    def save(self, *args, **kwargs):
        if self.is_active:
            Video.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
