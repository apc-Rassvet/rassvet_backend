"""Django management команда для импорта новостей из дампа SQL."""

import os
import re

from django.core.management.base import BaseCommand
from django.core.files import File
from django.utils.dateparse import parse_date

from content.models import News, Project, GalleryImage


def safe_str(val):
    """Приводит строковое значение к читаемому виду для дальнейшей обработки.

    - Убирает пустые и 'None'-подобные значения.
    - Удаляет внешние кавычки и экранирование,
      если строка обёрнута в одинарные кавычки.
    """
    val = val.strip()
    if val == "''" or val.lower() in ('none', 'nan'):
        return ''
    if val.startswith("'") and val.endswith("'"):
        return val[1:-1].replace("\\'", "'").replace('\\"', '"')
    return val


def safe_date(val):
    """Приводит строку к дате (или возвращает None), если это возможно.

    - Использует safe_str для предобработки.
    - Обрезает до 10 символов (YYYY-MM-DD).
    """
    val = safe_str(val)
    try:
        return parse_date(val[:10])
    except Exception:
        return None


def get_detail_page_type(ext_url, detail_text):
    """Определяет тип подробной страницы новости для поля detail_page_type.

    - Если есть внешняя ссылка, возвращает LINK.
    - Если есть detail_text, возвращает CREATE.
    - Если нет подробной страницы, возвращает NONE.
    """
    if ext_url:
        return News.DetailPageChoices.LINK
    if detail_text:
        return News.DetailPageChoices.CREATE
    return News.DetailPageChoices.NONE


def parse_sql_values_block(values_block, expected_fields=15):
    """Парсит SQL VALUES (...),(...); с учётом запятых, кавычек и переносов."""
    result = []
    current = []
    field = ''
    in_string = False
    escape = False
    paren_level = 0
    for char in values_block:
        if escape:
            field += char
            escape = False
        elif char == '\\':
            field += char
            escape = True
        elif char == "'":
            in_string = not in_string
            field += char
        elif char == ',' and not in_string and paren_level == 1:
            current.append(field.strip())
            field = ''
        elif char == '(' and not in_string:
            paren_level += 1
            if paren_level == 1:
                field = ''
                current = []
        elif char == ')' and not in_string:
            paren_level -= 1
            current.append(field.strip())
            field = ''
            if paren_level == 0:
                if len(current) == expected_fields:
                    result.append(current)
                else:
                    print(
                        f'!! Кортеж странной длины '
                        f'{len(current)}: {current[:3]} ... {current[-3:]}'
                    )
        else:
            field += char
    return result


class Command(BaseCommand):
    """Django management-команда для импорта новостей из SQL-дампа."""

    help = 'Импортирует новости из SQL-дампа'

    def handle(self, *args, **options):
        """Основной метод для выполнения команды импорта."""
        sql_path = 'data/dump.sql'
        images_dir = 'media_data/'

        with open(sql_path, encoding='utf-8') as f:
            sql = f.read()
        news_insert_re = re.compile(
            r'INSERT INTO [`\"]?news[`\"]? \([^)]+\) VALUES\s*(\(.*?\));',
            re.DOTALL | re.IGNORECASE,
        )
        matches = news_insert_re.findall(sql)
        if not matches:
            self.stdout.write(self.style.ERROR('Не найдено вставок новостей!'))
            return

        self.stdout.write(
            self.style.WARNING('Удаляем все новости и фотографии галерей...')
        )
        GalleryImage.objects.all().delete()
        News.objects.all().delete()
        count = 0
        for match in matches:
            news_tuples = parse_sql_values_block(match, expected_fields=15)
            for parts in news_tuples:
                (
                    nid,
                    ntype,
                    title,
                    short_text,
                    detail_text,
                    img_url,
                    date,
                    gallery,
                    video,
                    ext_url,
                    section_name,
                    section_url,
                    longread,
                    code,
                    project_id,
                ) = parts
                project = None
                pid = safe_str(project_id)
                if pid.isdigit() and int(pid) > 0:
                    project = Project.objects.filter(id=int(pid)).first()
                photo_file = None
                img = safe_str(img_url).lstrip('/')
                print(img)
                if img:
                    photo_path = os.path.join(images_dir, img)
                    if os.path.isfile(photo_path):
                        photo_file = File(open(photo_path, 'rb'))
                news = News(
                    title=safe_str(title),
                    date=safe_date(date),
                    summary=safe_str(short_text),
                    full_text=safe_str(detail_text),
                    detail_page_type=get_detail_page_type(
                        safe_str(ext_url), safe_str(detail_text)
                    ),
                    detail_page_link=safe_str(ext_url),
                    video_url=safe_str(video),
                    project=project,
                    show_on_main=True,
                )
                if photo_file:
                    news.photo.save(
                        os.path.basename(img), photo_file, save=False
                    )
                news.save()
                gal = safe_str(gallery)
                if gal:
                    images = re.split(r'[;,]', gal)
                    for img_path in images:
                        img_path = (
                            img_path.replace(r'\r\n', '').strip().lstrip('/')
                        )
                        if not img_path:
                            continue
                        gallery_img_path = os.path.join(images_dir, img_path)
                        if os.path.isfile(gallery_img_path):
                            with open(gallery_img_path, 'rb') as img_f:
                                gal_file = File(img_f)
                                img_filename = os.path.basename(img_path)
                                gal_img = GalleryImage(
                                    news=news, name=img_filename
                                )
                                gal_img.image.save(
                                    img_filename, gal_file, save=True
                                )
                                self.stdout.write(
                                    f'Добавлено фото в галерею: '
                                    f'{gal_img.image.url}'
                                )
                        else:
                            self.stdout.write(
                                self.style.WARNING(
                                    f'Фото галереи {img_path} не найдено.'
                                )
                            )
                self.stdout.write(
                    self.style.SUCCESS(f'Новость "{news.title}" импортирована')
                )
                count += 1
        self.stdout.write(
            self.style.SUCCESS(f'Импорт завершён. Всего новостей: {count}')
        )
