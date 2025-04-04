from django.db import models


def upload_file(instance, filename):
    """Метод для генерации пути к файлу."""
    return f'team/{instance.team_member.id}/{filename}'


class Team(models.Model):
    """Модель для хранения информации о членах команды."""

    name = models.CharField(max_length=255, verbose_name='ФИО')
    image = models.ImageField(upload_to='team', verbose_name='Фото')
    position = models.CharField(max_length=255, verbose_name='Должность')
    paginate = models.SmallIntegerField(verbose_name='Позиция на странице')
    discription = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Член команда'
        verbose_name_plural = 'Команда'


class TypeDocument(models.Model):
    """Типы документов."""

    type = models.CharField(max_length=255, verbose_name='Тип документа')

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Тип документа'
        verbose_name_plural = 'Типы документов'


class Document(models.Model):
    """Модель для хранения документов."""

    name = models.CharField(max_length=255, verbose_name='Название документа')
    file = models.FileField(
        upload_to=upload_file,
        verbose_name='Файл документа'
    )
    type = models.ForeignKey(
        TypeDocument, on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='Тип документа'
    )
    team_member = models.ForeignKey(
        Team, on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='Член команды'
    )
    on_main_page = models.BooleanField(
        default=False,
        verbose_name='Отображать на главной странице'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
