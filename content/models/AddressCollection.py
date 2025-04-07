from django.db import models


class AddressCollection(models.Model):
    """Модель Адресные сборы'."""

    STATUS_CHOICES = [
        ('active', 'Актуальный сбор'),
        ('completed', 'Завершенный сбор'),
    ]

    title = models.CharField(max_length=200, verbose_name="Заголовок*")
    short_description = models.TextField(verbose_name="Краткое описание*")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name="Статус сбора*"
    )
    collection_link = models.URLField(verbose_name="Ссылка на сбор*")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок сортировки",
        help_text="Чем меньше число, тем выше в списке"
    )

    class Meta:
        verbose_name = "Адресный сбор"
        verbose_name_plural = "Адресные сборы"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title
