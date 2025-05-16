"""Модуль содержит модели направлений деятельности, новостей и галереи.

Модели:
    - Direction: Хранит направления деятельности
    - News: Содержит информацию о новостях
    - GalleryImage: Хранит изображения для подробных страниц новостей
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from content.mixins import OrderMixin, TimestampMixin, TitleMixin


def upload_file(instance, filename):
    """Генерирует путь к файлу для загрузки."""
    return f'news_gallery_images/{instance.gallery_images.id}/{filename}'


class Direction(TimestampMixin, models.Model):
    """Модель направления деятельности, к которому может относиться новость."""

    name = models.CharField('Название', max_length=100, unique=True)

    class Meta:
        """Мета-настройки модели Direction."""

        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'

    def __str__(self):
        """Строковое представление направления."""
        return self.name


class News(TimestampMixin, TitleMixin, models.Model):
    """Модель новости, содержащая информацию и детализированные поля."""

    class DetailPageChoices(models.TextChoices):
        """Выбор способа отображения подробной страницы новости."""

        CREATE = 'create', 'Создать подробную страницу'
        LINK = 'link', 'Прикрепить ссылку'
        NONE = 'none', 'Не создавать страницу'

    photo = models.ImageField('Фото', upload_to='news_photos/')
    date = models.DateField('Дата новости', default=timezone.now)
    course_start = models.DateField('Старт курса', null=True, blank=True)
    summary = models.TextField('Краткий текст', max_length=255)
    directions = models.ManyToManyField('Направление деятельности', Direction)
    # project = models.ForeignKey(
    #     Project, on_delete=models.SET_NULL, null=True, blank=True
    # )
    detail_page_type = models.CharField(
        'Подробная страница',
        max_length=10,
        choices=DetailPageChoices.choices,
        default=DetailPageChoices.NONE,
    )
    detail_page_link = models.URLField(
        'Ссылка на подробную страницу', blank=True, null=True
    )
    show_on_main = models.BooleanField('Отображение на странице', default=True)
    full_text = models.TextField('Основной текст', blank=True, null=True)
    video_url = models.URLField('Ссылка на видео', blank=True, null=True)

    class Meta:
        """Мета-настройки модели News."""

        ordering = ['-date']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        """Строковое представление направления."""
        return f'{self.title} ({self.date})'

    def save(self, *args, **kwargs):
        """Сохранение объекта с предварительной валидацией."""
        self.clean()
        super().save(*args, **kwargs)

    def clean(self):
        """Валидация полей в зависимости от типа подробной страницы."""
        if self.detail_page_type == 'create' and not self.full_text:
            raise ValidationError(
                'Для создания подробной страницы '
                'необходимо заполнить основное описание.'
            )
        if self.detail_page_type == 'link' and not self.detail_page_link:
            raise ValidationError('Укажите ссылку на внешнюю страницу.')


class GalleryImage(OrderMixin, models.Model):
    """Модель изображений для галереи в карточке новости."""

    news = models.ForeignKey(
        'Новость',
        News,
        on_delete=models.CASCADE,
        related_name='gallery_images',
        verbose_name='Новость',
    )
    image = models.ImageField('Фото', upload_to=upload_file)

    class Meta:
        """Мета-настройки модели GalleryImage."""

        ordering = ['order', 'id']
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        """Строковое представление галереи."""
        return f'Галерея: {self.image.name}'
