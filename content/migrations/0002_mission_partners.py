# Generated by Django 4.2 on 2025-04-09 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('content', models.TextField(verbose_name='Основной текст')),
                ('image', models.ImageField(upload_to='missions/', verbose_name='Изображение')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Миссия',
                'verbose_name_plural': 'Миссии',
            },
        ),
        migrations.CreateModel(
            name='Partners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Обязательное поле', max_length=255, verbose_name='Название партнера*')),
                ('logo', models.ImageField(help_text='Обязательное поле', upload_to='partners/logos/', verbose_name='Логотип партнера*')),
                ('description', models.TextField(help_text='Обязательное поле', verbose_name='Описание*')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Партнер',
                'verbose_name_plural': 'Партнеры',
            },
        ),
    ]
