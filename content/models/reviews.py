from django.db import models

from content.constants import LENGTH_REVIEW_AUTHOR


class Review(models.Model):
    """Модель Отзывы (страница 'О нас')."""

    author_name = models.CharField(
        'Автор',
        max_length=LENGTH_REVIEW_AUTHOR,
    )
    content = models.TextField('Текст отзыва')
    order = models.PositiveIntegerField(
        'Порядок отображения',
        default=0,
        help_text='Чем меньше значение, тем первее в списке',
    )
    is_active = models.BooleanField('Активный', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.author_name
