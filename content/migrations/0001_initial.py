# Generated by Django 4.2 on 2025-04-06 23:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gratitude',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('content', models.TextField(blank=True, verbose_name='Содержание')),
                ('file', models.FileField(upload_to='gratitudes/', verbose_name='Файл благодарности')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активно')),
            ],
            options={
                'verbose_name': 'Благодарность',
                'verbose_name_plural': 'Благодарности',
                'ordering': ['order', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('url', models.URLField(validators=[django.core.validators.URLValidator()], verbose_name='Ссылка на видео')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активно')),
            ],
            options={
                'verbose_name': 'Видео',
                'verbose_name_plural': 'Видео',
                'ordering': ['-created_at'],
            },
        ),
    ]
