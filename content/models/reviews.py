from django.db import models

from content.constants import LENGTH_REVIEW_TITLE, LENGTH_REVIEW_AUTHOR


class Review(models.Model):
    """Модель Отзывы (страница 'О нас')."""

    title = models.CharField('Заголовок', max_length=LENGTH_REVIEW_TITLE)
    content = models.TextField('Текст отзыва')
    author_name = models.CharField(
        'Имя автора',
        max_length=LENGTH_REVIEW_AUTHOR,
        blank=True,
        null=True,
        default=None
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    is_active = models.BooleanField('Активный', default=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
