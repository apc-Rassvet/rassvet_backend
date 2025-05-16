"""Модуль содержит модели направлений деятельности, новостей и галереи.

Модели:
    - Direction: Хранит направления деятельности
    - News: Содержит информацию о новостях
    - GalleryImage: Хранит изображения для подробных страниц новостей
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from content.mixins import TimestampMixin


class Direction(TimestampMixin, models.Model):
    """Модель направления деятельности, к которому может относиться новость."""

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        """Строковое представление направления."""
        return self.name


class GalleryImage(models.Model):
    """Модель изображений для галереи в карточке новости."""

    image = models.ImageField(upload_to='news_gallery_images/')

    def __str__(self):
        """Строковое представление направления."""
        return f'Галерея: {self.image.name}'


class News(models.Model):
    """Модель новости, содержащая информацию и детализированные поля."""

    class DetailPageChoices(models.TextChoices):
        """Выбор способа отображения подробной страницы новости."""

        CREATE = 'create', 'Создать подробную страницу'
        LINK = 'link', 'Прикрепить ссылку'
        NONE = 'none', 'Не создавать страницу'

    class DisplayChoices(models.TextChoices):
        """Выбор отображения новости на главной странице."""

        YES = 'True', 'Да'
        NO = 'False', 'Нет'

    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='news_photos/')
    date = models.DateField(default=timezone.now)
    course_start = models.DateField(null=True, blank=True)
    summary = models.TextField()
    directions = models.ManyToManyField(Direction)
    # project = models.ForeignKey(
    #     Project, on_delete=models.SET_NULL, null=True, blank=True
    # )
    detail_page_type = models.CharField(
        max_length=10,
        choices=DetailPageChoices.choices,
        default=DetailPageChoices.NONE,
    )
    detail_page_link = models.URLField(blank=True, null=True)
    show_on_main = models.BooleanField(default=True)
    order = models.PositiveIntegerField(
        default=0, help_text='Используется для сортировки карточек'
    )
    full_text = models.TextField(blank=True, null=True)
    gallery = models.ForeignKey(GalleryImage, blank=True)
    video_url = models.URLField(blank=True, null=True)

    class Meta:
        """Мета-настройки модели News."""

        ordering = ['-order', '-date']

    def __str__(self):
        """Строковое представление направления."""
        return f'{self.title} ({self.date})'

    def clean(self):
        """Валидация полей в зависимости от типа подробной страницы."""
        if self.detail_page_type == 'create' and not self.full_text:
            raise ValidationError(
                'Для создания подробной страницы '
                'необходимо заполнить основное описание.'
            )
        if self.detail_page_type == 'link' and not self.detail_page_link:
            raise ValidationError('Укажите ссылку на внешнюю страницу.')

    def save(self, *args, **kwargs):
        """Сохранение объекта с предварительной валидацией."""
        self.clean()
        super().save(*args, **kwargs)
