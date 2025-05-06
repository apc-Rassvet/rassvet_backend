from django.db import models


class Page(models.Model):
    """Модель для хранения информации о страницах сайта."""

    PAGE_CHOICES = (
        ('aba-therapy', 'ABA-терапия'),
        ('adaptive-physical-culture', 'Адаптивная физкультура'),
        ('creative-workshops', 'Творческие мастерские'),
        ('resource-classes', 'Ресурсные классы'),
        ('children-leisure', 'Досуг для детей'),
    )
    name = models.SlugField(
        max_length=255,
        choices=PAGE_CHOICES,
        unique=True,
        verbose_name='Направление деятельности',
    )

    class Meta:
        verbose_name = 'Страница помощи детям'
        verbose_name_plural = 'Страницы помощи детям'

    def __str__(self):
        return self.get_name_display()


class Supervisor(models.Model):
    """Модель для хранения информации о Супервизоров центра."""

    name = models.CharField(max_length=255, verbose_name='ФИО')
    image = models.ImageField(upload_to='supervisors/', verbose_name='Фото')
    position = models.CharField(max_length=255, verbose_name='Должность')
    ordering = models.PositiveSmallIntegerField(
        default=0, verbose_name='Порядок'
    )
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        verbose_name='Страница',
        related_name='supervisor',
    )

    class Meta:
        verbose_name = 'Супервизор'
        verbose_name_plural = 'Супервизоры'
        ordering = ['ordering']

    def __str__(self):
        return self.name
