from django.db import models


def upload_file(instance, filename):
    """Метод для генерации пути к файлу."""
    return f'team/{instance.team_member.id}/{filename}'


class Employee(models.Model):
    """Модель для хранения информации о членах команды."""

    name = models.CharField(max_length=255, verbose_name='ФИО')
    image = models.ImageField(upload_to='team', verbose_name='Фото')
    position_full = models.CharField(
        max_length=255,
        verbose_name='Полная должность сотрудника'
    )
    position_short = models.CharField(
        max_length=255,
        verbose_name='Сокращенная должность сотрудника'
    )
    ordaring = models.SmallIntegerField(verbose_name='Позиция на странице')
    education = models.TextField(verbose_name='Образование', blank=True)
    additional_education = models.TextField(
        verbose_name='Дополнительное образование', 
        blank=True
    )
    trainings = models.TextField(verbose_name='Тренинги', blank=True)
    interviews = models.URLField(verbose_name='Интервью', blank=True)
    category_on_main = models.BooleanField(
        default=False,
        verbose_name='Отображать категории документов на главной странице'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


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
        verbose_name='Файл документа',
    )
    type = models.ForeignKey(
        TypeDocument, on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='Тип документа'
    )
    team_member = models.ForeignKey(
        Employee, on_delete=models.CASCADE,
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