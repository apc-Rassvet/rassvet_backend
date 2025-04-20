from django.db import models
from content.constants import LENGTH_GRATITUDE_TITLE


class Gratitude(models.Model):
    """Модель для 'Благодарности' в разделе 'О нас'."""

    title = models.CharField('Заголовок', max_length=LENGTH_GRATITUDE_TITLE)
    description = models.TextField('Описание', blank=True)
    file = models.FileField('Файл благодарности', upload_to='gratitudes/')
    order = models.PositiveIntegerField(
        'Порядок отображения',
        default=0,
        help_text='Чем меньше значение, тем первее в списке',
    )
    is_active = models.BooleanField('Видимость в ленте', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Благодарность'
        verbose_name_plural = 'Благодарности'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title
