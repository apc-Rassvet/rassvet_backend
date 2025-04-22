from django.db import models


def upload_file(instance, filename):
    """Метод для генерации пути к файлу."""
    return f'team/{instance.team_member.id}/{filename}'


class Employee(models.Model):
    """Модель для хранения информации о членах команды."""

    name = models.CharField(max_length=255, verbose_name='ФИО')
    image = models.ImageField(upload_to='team', verbose_name='Фото')
    ordaring = models.SmallIntegerField(
        verbose_name='Позиция на общей странице'
    )
    interviews = models.URLField(verbose_name='Интервью', blank=True)
    specialists_register = models.URLField(
        verbose_name='Реестр специалистов',
        blank=True
    )
    category_on_main = models.BooleanField(
        default=False,
        verbose_name='Отображать категории документов на главной странице'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Speciality(models.Model):
    """Модель специальностей сотрудников."""

    speciality = models.CharField(
        max_length=255,
        verbose_name='Название специальности',
        help_text='Укажите должность сотрудника'
    )
    team_member = models.ForeignKey(
        Employee, on_delete=models.CASCADE,
        related_name='specialities',
        verbose_name='Член команды'
    )
    on_main = models.BooleanField(
        default=True,
        verbose_name='Отображать на общей странице'
    )
    position = models.SmallIntegerField(
        default=1,
        verbose_name='Позиция на странице',
        help_text=(
            'Позиция определяет в каком порядке'
            ' будут располагаться специальности'
        )
    )


class Education(models.Model):
    """Модель специальностей сотрудников."""

    education = models.TextField(
        verbose_name='Образование'
    )
    team_member = models.ForeignKey(
        Employee, on_delete=models.CASCADE,
        related_name='education',
        verbose_name='Член команды'
    )
    position = models.SmallIntegerField(
        default=1,
        verbose_name='Позиция на странице',
    )


class AdditionalEducation(models.Model):
    """Модель специальностей сотрудников."""

    additional_education = models.TextField(
        verbose_name='Дополнительное образование'
    )
    team_member = models.ForeignKey(
        Employee, on_delete=models.CASCADE,
        related_name='additional_education',
        verbose_name='Член команды'
    )
    position = models.SmallIntegerField(
        default=1,
        verbose_name='Позиция на странице',
    )


class Trainings(models.Model):
    """Модель специальностей сотрудников."""

    trainings = models.TextField(
        verbose_name='Тренинги'
    )
    team_member = models.ForeignKey(
        Employee, on_delete=models.CASCADE,
        related_name='trainings',
        verbose_name='Член команды'
    )
    position = models.SmallIntegerField(
        default=1,
        verbose_name='Позиция на странице',
    )


class TypeDocument(models.Model):
    """Модель для хранения типов документов."""

    name = models.CharField(
        max_length=255,
        verbose_name='Название типа документа'
    )

    def __str__(self):
        return self.name


class Document(models.Model):
    """Модель для хранения документов."""

    name = models.CharField(
        max_length=255,
        verbose_name='Название документа'
    )
    file = models.FileField(
        upload_to=upload_file,
        verbose_name='Файл документа',
    )
    type = models.ForeignKey(
        TypeDocument,
        on_delete=models.CASCADE,
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
