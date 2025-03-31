from django.db import models
from django.core.validators import URLValidator


class Video(models.Model):
    """Модель для 'Видео' в разделе 'О нас'"""
    title = models.CharField('Заголовок', max_length=200)
    url = models.URLField('Ссылка на видео', validators=[URLValidator()])
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    is_active = models.BooleanField('Активно', default=True)

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Gratitude(models.Model):
    """Модель для 'Благодарности' в разделе 'О нас'"""
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Содержание', blank=True)
    author = models.CharField('Автор', max_length=100)
    file = models.FileField('Файл благодарности', upload_to='testimonials/')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    order = models.PositiveIntegerField('Порядок отображения', default=0)
    is_active = models.BooleanField('Активно', default=True)

    class Meta:
        verbose_name = 'Благодарность'
        verbose_name_plural = 'Благодарности'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title
