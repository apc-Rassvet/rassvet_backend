from django.db import models


def upload_file(instance, filename):
    """Метод для генерации пути к файлу."""
    return f'team/{instance.team_member.id}/{filename}'


class Employee(models.Model):
    """Модель для хранения информации о членах команды."""

    name = models.CharField(max_length=255, verbose_name='ФИО')
    image = models.ImageField(upload_to='team', verbose_name='Фото')
    speciality_1 = models.CharField(
        max_length=255,
        verbose_name='Специальность 1 (Видна везде)'
    )
    speciality_2 = models.CharField(
        max_length=255,
        verbose_name='Специальность 2 (Видна только на странице сотрудника)'
    )
    speciality_3 = models.CharField(
        max_length=255,
        verbose_name='Специальность 3 (Видна только на странице сотрудника)'
    )
    ordaring = models.SmallIntegerField(
        verbose_name='Позиция на общей странице'
    )
    education_1 = models.TextField(
        verbose_name='Образование 1', blank=True
    )
    education_2 = models.TextField(
        verbose_name='Образование 2', blank=True
    )
    education_3 = models.TextField(
        verbose_name='Образование 3', blank=True
    )
    additional_education_1 = models.TextField(
        verbose_name='Дополнительное образование 1',
        blank=True
    )
    additional_education_2 = models.TextField(
        verbose_name='Дополнительное образование 2',
        blank=True
    )
    additional_education_3 = models.TextField(
        verbose_name='Дополнительное образование 3',
        blank=True
    )
    additional_education_4 = models.TextField(
        verbose_name='Дополнительное образование 4',
        blank=True
    )
    additional_education_5 = models.TextField(
        verbose_name='Дополнительное образование 5',
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
