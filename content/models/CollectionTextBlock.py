from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from content.models.addressCollection import AddressCollection


class CollectionTextBlock(models.Model):
    """Модель Текстовый блок коллекции'."""

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