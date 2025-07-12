"""Модуль содержит модели, связанные с Базой знаний.

Модели:
    1. ChapterKnowledgeBase: Модель разделов Базы знаний
    2. Article: Модель статьи Базы знаний
    3. ArticleTextBlock: Текстовый блок статьи Базы знаний
    4. ArticleGallery: Галерея фото статьи Базы знаний
"""

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from content.constants import IMAGE_CONTENT_TYPES
from content.mixins import TitleMixin
from content.utils import ckeditor_function


def upload_file(instance, filename):
    """Генерирует путь к файлу для загрузки."""
    return f'{instance.__class__.__name__}/{instance.article.id}/{filename}'


class ChapterKnowledgeBase(TitleMixin, models.Model):
    """Модель разделов Базы знаний."""

    class Meta:
        """Класс Meta для ChapterKnowledgeBase, содержащий мета-данные."""

        verbose_name = 'Раздел'
        verbose_name_plural = 'База знаний - разделы'
        ordering = ('title',)

    def __str__(self):
        """Возвращает строковое представление ChapterKnowledgeBase."""
        return self.title


class Article(TitleMixin, models.Model):
    """Модель статьи Базы знаний."""

    class DetailedPageChoices(models.TextChoices):
        """Выбор подробной страницы."""

        DETAILED = 'detailed', 'База знаний подробная'
        LINK = 'link', 'Ссылка на существующую страницу'

    chapter = models.ForeignKey(
        ChapterKnowledgeBase,
        on_delete=models.CASCADE,
        related_name='article',
        verbose_name='Раздел Базы знаний',
    )
    detailed_page = models.CharField(
        max_length=max(len(value) for value, _ in DetailedPageChoices.choices),
        choices=DetailedPageChoices.choices,
        verbose_name='Выбор подробной страницы',
    )
    link = models.URLField(
        verbose_name='Ссылка на существующую страницу',
        blank=True,
    )
    video_link = models.URLField(
        verbose_name='Ссылка на видео',
        blank=True,
    )

    class Meta:
        """Класс Meta для Article, содержащий мета-данные."""

        verbose_name = 'Статья'
        verbose_name_plural = 'База знаний - статьи'
        ordering = ('title',)

    def __str__(self):
        """Возвращает строковое представление Article."""
        return self.title

    def clean(self):
        """Валидация поля link в зависмисти от выбора в поле detailed_page."""
        if self.detailed_page == 'link' and self.link == '':
            raise ValidationError('Заполни "Ссылка на существующую страницу".')


class ArticleTextBlock(models.Model):
    """Текстовый блок статьи Базы знаний."""

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='text_block',
        verbose_name='статья',
    )
    text = ckeditor_function(verbose_name='текст статьи')
    foto = models.ImageField(
        upload_to=upload_file,
        verbose_name='Фотография',
        validators=[FileExtensionValidator(IMAGE_CONTENT_TYPES)],
        blank=True,
    )

    class Meta:
        """Класс Meta для ArticleTextBlock, содержащий мета-данные."""

        verbose_name = 'Текстовый блок статьи Базы знаний'
        verbose_name_plural = 'Текстовые блоки статьи Базы знаний'

    def __str__(self):
        """Возвращает строковое представление статьи текстового блока."""
        return f'Фотография для проекта {self.article.title}'


class ArticleGallery(models.Model):
    """Галерея фото статьи Базы знаний."""

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='gallery',
        verbose_name='статья',
    )
    foto = models.ImageField(
        upload_to=upload_file,
        verbose_name='Фотография',
        validators=[FileExtensionValidator(IMAGE_CONTENT_TYPES)],
    )

    class Meta:
        """Класс Meta для ArticleTextBlock, содержащий мета-данные."""

        verbose_name = 'Фото статьи Базы знаний'
        verbose_name_plural = 'Галерея фотграфий статьи Базы знаний'

    def __str__(self):
        """Возвращает строковое представление статьи текстового блока."""
        return f'Фотография для проекта {self.article.title}'
