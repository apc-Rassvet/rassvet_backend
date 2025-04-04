# Generated by Django 4.2 on 2025-04-04 08:39

import api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='ФИО')),
                ('image', models.ImageField(upload_to='team', verbose_name='Фото')),
                ('position', models.CharField(max_length=255, verbose_name='Должность')),
                ('paginate', models.SmallIntegerField(verbose_name='Позиция на странице')),
                ('discription', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Член команда',
                'verbose_name_plural': 'Команда',
            },
        ),
        migrations.CreateModel(
            name='TypeDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255, verbose_name='Тип документа')),
            ],
            options={
                'verbose_name': 'Тип документа',
                'verbose_name_plural': 'Типы документов',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название документа')),
                ('file', models.FileField(upload_to=api.models.upload_file, verbose_name='Файл документа')),
                ('on_main_page', models.BooleanField(default=False, verbose_name='Отображать на главной странице')),
                ('team_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='api.team', verbose_name='Член команды')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='api.typedocument', verbose_name='Тип документа')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
            },
        ),
    ]
