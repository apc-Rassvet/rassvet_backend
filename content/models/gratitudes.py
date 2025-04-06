from django.db import models
from ..constants import LENGTH_GRATITUDE_TITLE, DEFAULT_GRATITUDE_ORDER


class Gratitude(models.Model):
    """Модель для 'Благодарности' в разделе 'О нас'."""

    title = models.CharField('Заголовок', max_length=LENGTH_GRATITUDE_TITLE)
    content = models.TextField('Содержание', blank=True)
    file = models.FileField('Файл благодарности', upload_to='gratitudes/')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    order = models.PositiveIntegerField(
        'Порядок отображения', default=DEFAULT_GRATITUDE_ORDER
    )
    is_active = models.BooleanField('Активно', default=True)

    class Meta:
        verbose_name = 'Благодарность'
        verbose_name_plural = 'Благодарности'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title
