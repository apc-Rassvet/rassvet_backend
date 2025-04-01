from django.db import models


class Team(models.Model):
    """Модель для хранения информации о членах команды."""

    name = models.CharField(max_length=255, verbose_name='ФИО')
    image = models.ImageField(upload_to='team', verbose_name='Фото')
    position = models.CharField(max_length=255, verbose_name='Должность')
    telephone = models.CharField(max_length=20, verbose_name='Телефон')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Член команда'
        verbose_name_plural = 'Команда'


def upload_file(instance, filename):
    """Метод для генерации пути к файлу."""
    return f'documents/{instance.team_member.id}/{filename}'


class Document(models.Model):
    """Модель для хранения документов."""

    name = models.CharField(max_length=255, verbose_name='Название документа')
    file = models.FileField(
        upload_to=upload_file,
        verbose_name='Файл документа'
    )
    team_member = models.ForeignKey(
        Team, on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='Член команды'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
