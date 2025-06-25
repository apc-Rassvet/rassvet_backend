"""Модуль содержит модели, связанные с Базой знаний.

Модели:
    1. ChapterKnowledgeBase: Модель разделов Базы знаний
    2. Article: Модель статьи Базы знаний
    3. ArticleTextBlock: Текстовый блок статьи Базы знаний
"""

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from ordered_model.models import OrderedModel

from content.constants import (
    CHAR_FIELD_LENGTH,
    IMAGE_CONTENT_TYPES,
    VIDEO_CONTENT_TYPES,
)
from content.mixins import TitleMixin
from content.utils import ckeditor_function


class ChapterKnowledgeBase(TitleMixin, OrderedModel):
    """Модель разделов Базы знаний."""

    class Meta(OrderedModel.Meta):
        """Класс Meta для ChapterKnowledgeBase, содержащий мета-данные."""

        verbose_name = 'Раздел Базы знаний'
        verbose_name_plural = 'Разделы Базы знаний'


class Article(TitleMixin, OrderedModel):
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
    detailed_knowledge_base = models.CharField(
        max_length=CHAR_FIELD_LENGTH,
        verbose_name='База знаний подробная',
        blank=True,
        null=True,
    )
    link = models.URLField(
        verbose_name='Ссылка на существующую страницу',
        blank=True,
        null=True,
    )
    gallery = models.ImageField(
        upload_to='article/',
        verbose_name='Фотография',
        validators=[FileExtensionValidator(IMAGE_CONTENT_TYPES)],
    )

    class Meta(OrderedModel.Meta):
        """Класс Meta для Article, содержащий мета-данные."""

        verbose_name = 'Статья Базы знаний'
        verbose_name_plural = 'Статьи Базы знаний'

    def __str__(self):
        """Возвращает строковое представление Article."""
        return self.title

    def clean(self):
        """Валидация поля link_button в зависмисти от выбора в поле button."""
        if (
            self.detailed_page == 'detailed'
            and self.detailed_knowledge_base is None
        ):
            raise ValidationError('Заполни "База знаний подробная".')
        if self.detailed_page == 'link' and self.link is None:
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
        upload_to='article/',
        verbose_name='Фотография',
        validators=[FileExtensionValidator(IMAGE_CONTENT_TYPES)],
        blank=True,
        null=True,
    )
    video = models.FileField(
        upload_to='article/',
        verbose_name='Видео',
        validators=[FileExtensionValidator(VIDEO_CONTENT_TYPES)],
        blank=True,
        null=True,
    )
    video_link = models.URLField(
        verbose_name='Ссылка на видео',
        blank=True,
        null=True,
    )

    class Meta:
        """Класс Meta для ArticleTextBlock, содержащий мета-данные."""

        verbose_name = 'Текстовый блок статьи Базы знаний'

    def __str__(self):
        """Возвращает строковое представление статьи текстового блока."""
        return f'Фотография для проекта {self.article.title}'
