from django.db import models


class Partner(models.Model):
    """Модель Партнеры (страница Партнеры)."""

    name = models.CharField(
        max_length=255,
        verbose_name='Название партнера*',
        help_text='Обязательное поле',
    )
    logo = models.ImageField(
        upload_to='partners/logos/',
        verbose_name='Логотип партнера*',
        help_text='Обязательное поле',
    )
    description = models.TextField(
        verbose_name='Описание*', help_text='Обязательное поле'
    )
    order = models.PositiveIntegerField(
        'Порядок отображения',
        default=0,
        help_text='Чем меньше значение, тем первее в списке',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name
