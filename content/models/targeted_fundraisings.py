from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class FundraisingStatus(models.TextChoices):
    ACTIVE = 'active', 'Актуальный сбор'
    COMPLETED = 'completed', 'Завершенный сбор'


class TargetedFundraising(models.Model):
    """Модель для 'Адресные сборы'."""

    title = models.CharField(max_length=200, verbose_name="Заголовок*")
    short_description = models.TextField(verbose_name="Краткое описание*")
    status = models.CharField(
        max_length=10,
        choices=FundraisingStatus.choices,
        default=FundraisingStatus.ACTIVE,
        verbose_name="Статус сбора*",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок сортировки",
        help_text="Чем меньше число, тем выше в списке",
    )

    class Meta:
        verbose_name = "Адресный сбор"
        verbose_name_plural = "Адресные сборы"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def clean(self):
        if self.order < 0:
            raise ValidationError(
                {'order': 'Порядок сортировки не может быть меньше нуля'}
            )
        return super().clean()


class FundraisingPhoto(models.Model):
    """Модель для 'Фотографий'."""

    fundraising = models.ForeignKey(
        TargetedFundraising, on_delete=models.CASCADE, related_name='photos'
    )
    image = models.ImageField(
        upload_to='fundraisings/',
        verbose_name="Фотография",
        blank=False,
        null=False,
    )
    position = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        help_text="Позиция фотографии (1-3)",
    )

    class Meta:
        verbose_name = "Фотография сбора"
        verbose_name_plural = "Фотографии сборов"
        ordering = ['position']
        unique_together = ('fundraising', 'position')

    def __str__(self):
        return f"Фотография {self.position} для {self.fundraising.title}"


class FundraisingTextBlock(models.Model):
    """Модель Текстовый блок коллекции'."""

    fundraising = models.ForeignKey(
        TargetedFundraising,
        on_delete=models.CASCADE,
        related_name='text_blocks',
    )
    title = models.CharField(
        max_length=200, blank=True, verbose_name="Заголовок блока"
    )
    content = models.TextField(
        verbose_name="Текстовый блок", blank=False, null=False
    )
    position = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        verbose_name="Позиция блока (1-3)",
    )

    class Meta:
        verbose_name = "Текстовый блок"
        verbose_name_plural = "Текстовые блоки"
        ordering = ['position']
        unique_together = ('fundraising', 'position')

    def __str__(self):
        return f"Текстовый блок {self.position} для {self.fundraising.title}"
