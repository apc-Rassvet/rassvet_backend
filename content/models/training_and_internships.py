"""Модуль содержит модели относящиеся к обучению и стажировкам.

Модели:
    - FormatStudy: Перечисление фозможных форматов обученя
    - ActionOmButton: Перечисление действий при нажатии на кнопку
    - TrainingAndInternships: Содержит информацию об обучениях и стажировках
    - TAIPhoto: Хранит фотографии карточек обучения и стажировок
"""

from django.core.validators import FileExtensionValidator
from django.db import models
from ordered_model.models import OrderedModel

from content.constants import IMAGE_CONTENT_TYPES
from content.mixins import TitleMixin
from content.utils import ckeditor_function

from .news import News


class FormatStudy(models.TextChoices):
    """Формат учебы"""

    ONLINE = 'online', 'Онлайн'
    OFFLINE = 'offline', 'Оффлайн'
    HYBRID = 'hybrid', 'Гибридный'


class ActionOmButton(models.TextChoices):
    """Действие кнопки"""

    DETEIL = 'deteil', 'Подробная страница'
    REGISTRATION = 'registration', 'Форма регистрации и отклика'
    URL_NEWS = 'url', 'Ссылка на новость'


class TrainingAndInternships(TitleMixin, OrderedModel):
    """Модель обучения и стажировки."""

    add_info = models.CharField(
        max_length=25,
        verbose_name='Дополнительная информация',
        blank=True,
    )
    info = ckeditor_function(verbose_name='Дополнительная информация')
    price = models.IntegerField(
        verbose_name='Цена',
        null=True,
    )
    date = models.DateField(
        verbose_name='Дата',
    )
    format_study = models.CharField(
        max_length=max(len(value) for value, _ in FormatStudy.choices),
        choices=FormatStudy.choices,
        default=FormatStudy.ONLINE,
        verbose_name='Формат обучения',
    )
    location = models.CharField(
        max_length=255,
        verbose_name='Место проведения',
        blank=True,
    )
    short_description = ckeditor_function(verbose_name='Краткое описание')
    text = ckeditor_function(verbose_name='Текстовый блок')
    text_on_button = models.CharField(
        max_length=255,
        verbose_name='Текст на кнопке',
        blank=True,
    )
    action_on_button = models.CharField(
        max_length=max(len(value) for value, _ in ActionOmButton.choices),
        choices=ActionOmButton.choices,
        default=ActionOmButton.DETEIL,
        verbose_name='Действие на кнопке',
    )
    linked_news = models.ForeignKey(
        News,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Ссылка на новость',
        blank=True,
        null=True,
    )

    class Meta(OrderedModel.Meta):
        """Класс Meta для TrainingAndInternships, содержащий мета-данные."""

        verbose_name = 'Обучение и стажировка'
        verbose_name_plural = 'Обучение и стажировки'
        ordering = ['order']


    def __str__(self):
        """Возвращает строковое представление обучения и стажировок."""
        return self.title


class TAIPhoto(models.Model):
    """Модель Фотографий обучения и стажировок."""

    training = models.ForeignKey(
        TrainingAndInternships,
        on_delete=models.CASCADE,
        related_name='photo',
        verbose_name='Обучение и стажировка',
    )
    image = models.ImageField(
        upload_to='training/',
        verbose_name='Фотография',
        validators=[FileExtensionValidator(IMAGE_CONTENT_TYPES)],
        blank=False,
        null=False,
    )
    on_main = models.BooleanField(
        default=False,
        verbose_name='На главной странице',
    )

    class Meta:
        """Класс Meta для TAIPhoto, содержащий мета-данные."""

        verbose_name = 'Фотография карточки обучения и стажировок'
        verbose_name_plural = 'Фотографии карточек обучения и стажировок'

    def __str__(self):
        """Возвращает строковое представление  фотографии."""
        return f'Фотография для карточки {self.training.title}'
