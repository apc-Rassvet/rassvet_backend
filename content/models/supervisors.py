from django.db import models


class Supervisor(models.Model):
    """Модель для хранения информации о Супервизоров центра."""

    name = models.CharField(max_length=255, verbose_name='ФИО')
    image = models.ImageField(upload_to='supervisors/', verbose_name='Фото')
    position = models.CharField(max_length=255, verbose_name='Должность')
    ordering = models.PositiveSmallIntegerField(
        default=0, verbose_name='Порядок'
    )
    PAGE_CHOICES = (
        ('aba-therapy', 'ABA-терапия'),
        ('adaptive-physical-culture', 'Адаптивная физкультура'),
        ('creative-workshops', 'Творческие мастерские'),
        ('resource-classes', 'Ресурсные классы'),
        ('children-leisure', 'Досуг для детей'),
    )
    page = models.SlugField(
        max_length=255,
        choices=PAGE_CHOICES,
        verbose_name='Направление деятельности',
    )

    class Meta:
        verbose_name = 'Супервизор'
        verbose_name_plural = 'Супервизоры'
        ordering = ['ordering']

    def __str__(self):
        return self.name
