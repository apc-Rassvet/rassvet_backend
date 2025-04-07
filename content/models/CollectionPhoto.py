from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from content.models.addressCollection import AddressCollection


class CollectionPhoto(models.Model):
    """Модель Фото блок коллекции'."""

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
