"""Модуль содержит модели относящиеся к обучению и стажировкам.

Модели:
    - FormatStudy: Перечисление фозможных форматов обученя
    - ActionOmButton: Перечисление действий при нажатии на кнопку
    - TrainingAndInternships: Содержит информацию об обучениях и стажировках
    - TAIPhoto: Хранит фотографии карточек обучения и стажировок
"""

from django.core.validators import FileExtensionValidator
from django.db import models
from django.forms import ValidationError
from ordered_model.models import OrderedModel

from content.constants import IMAGE_CONTENT_TYPES
from content.mixins import TitleMixin
from content.utils import ckeditor_function


class FormatStudy(models.TextChoices):
    """Формат учебы."""

    ONLINE = 'online', 'Онлайн'
    OFFLINE = 'offline', 'Оффлайн'
    HYBRID = 'hybrid', 'Гибридный'


class ActionOnButton(models.TextChoices):
    """Действие кнопки."""

    DETAIL = 'detail', 'Подробная страница'
    REGISTRATION = 'registration', 'Форма регистрации и отклика'
    URL_NEWS = 'url', 'Ссылка на новость'


class TrainingAndInternships(TitleMixin, OrderedModel):
    """Модель обучения и стажировки."""

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    add_info = models.CharField(
        max_length=25,
        verbose_name='Плашка с дополнительной информацией ',
        blank=True,
    )
    price = models.CharField(
        max_length=255,
        verbose_name='Цена',
        blank=True,
    )
    date = models.CharField(
        verbose_name='Дата',
        max_length=255,
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
    short_description = models.TextField(verbose_name='Краткое описание')
    text = ckeditor_function(blank=True, verbose_name='Текстовый блок')
    text_on_button = models.CharField(
        max_length=255,
        verbose_name='Текст на кнопке',
        blank=True,
    )
    action_on_button = models.CharField(
        max_length=max(len(value) for value, _ in ActionOnButton.choices),
        choices=ActionOnButton.choices,
        default=ActionOnButton.DETAIL,
        verbose_name='Действие на кнопке',
    )
    linked_news = models.URLField(
        verbose_name='Произвольная ссылка',
        blank=True,
        null=True,
        max_length=200,
    )

    class Meta(OrderedModel.Meta):
        """Класс Meta для TrainingAndInternships, содержащий мета-данные."""

        verbose_name = 'Обучение и стажировка'
        verbose_name_plural = 'Обучение и стажировки'
        ordering = ['order']

    def __str__(self):
        """Возвращает строковое представление обучения и стажировок."""
        return self.title

    def validate(self, data):
        """Валидация полей модели."""
        action_on_button = data.get(
            'action_on_button',
            self.instance.action_on_button if self.instance else None,
        )
        text_value = data.get(
            'text', self.instance.text if self.instance else None
        )
        linked_news = data.get(
            'linked_news', self.instance.linked_news if self.instance else None
        )
        if action_on_button == ActionOnButton.DETAIL and not text_value:
            raise ValidationError('Текстовый блок не может быть пустым')
        elif action_on_button == ActionOnButton.URL_NEWS and not linked_news:
            raise ValidationError('Ссылка на новость не может быть пустой')
        return data


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
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок отображения',
    )

    class Meta:
        """Класс Meta для TAIPhoto, содержащий мета-данные."""

        verbose_name = 'Фотография карточки обучения и стажировок'
        verbose_name_plural = 'Фотографии карточек обучения и стажировок'

    def __str__(self):
        """Возвращает строковое представление  фотографии."""
        return f'Фотография для карточки {self.training.title}'
