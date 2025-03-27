from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class AddressCollection(models.Model):
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


class CollectionPhoto(models.Model):
    collection = models.ForeignKey(
        AddressCollection,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    image = models.ImageField(
        upload_to='collections/',
        verbose_name="Фото"
    )
    position = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        help_text="Позиция фото (1-3)"
    )

    class Meta:
        verbose_name = "Фото сбора"
        verbose_name_plural = "Фото сборов"
        ordering = ['position']

    def __str__(self):
        return f"Фото {self.position} для {self.collection.title}"


class CollectionTextBlock(models.Model):
    collection = models.ForeignKey(
        AddressCollection,
        on_delete=models.CASCADE,
        related_name='text_blocks'
    )
    title = models.CharField(max_length=200, blank=True, verbose_name="Заголовок блока")
    content = models.TextField(verbose_name="Текстовый блок")
    position = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        verbose_name="Позиция блока (1-3)"
    )

    class Meta:
        verbose_name = "Текстовый блок"
        verbose_name_plural = "Текстовые блоки"
        ordering = ['position']

    def __str__(self):
        return f"Текстовый блок {self.position} для {self.collection.title}"
