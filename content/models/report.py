from django.db import models
from django.utils import timezone


def upload_file(instance, filename):
    """Метод для генерации пути к файлу."""
    return f'reports/{instance.chapter.id}/{filename}'


class Chapter(models.Model):
    title = models.TextField(
        verbose_name='Название раздела')
    position = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Позиция на странице')

    class Meta:
        verbose_name = 'Раздел отчетов'
        verbose_name_plural = 'Разделы отчетов'

    def __str__(self):
        return self.title


class Report(models.Model):
    title = models.TextField(
        verbose_name='Название отчета'
    )
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name='Раздел'
    )
    pub_date = models.DateField(
        default=timezone.now,
        verbose_name='Дата публикации',
        help_text='Публикации сортируются от новых к старым'
    )
    file = models.FileField(
        upload_to=upload_file,
        verbose_name='Файл отчета'
    )
    download_icon = models.BooleanField(
        default=True,
        verbose_name='Иконка скачивания'
    )

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'

    def __str__(self):
        return self.title
