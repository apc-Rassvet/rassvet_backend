"""Django management команда для импорта новостей из дампа SQL."""

from datetime import date
import re
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from content.models import (
    News,
    Project,
    Direction,
    GalleryImage,
)
from content.management.utils import (
    clean_media_path,
    parse_sql_tuples,
    split_gallery,
)


class Command(BaseCommand):
    """Django management команда для импорта новостей из дампа SQL."""

    help = 'Импортирует новости с галереей из дампа SQL'

    def handle(self, *args, **options):
        """Основной метод команды."""
        sql_file = 'data/rassvet_dump.sql'
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_dump = f.read()
        news_items = self.extract_news(sql_dump)
        created, skipped = 0, 0

        for n in news_items:
            project = None
            if n['project_id'] and n['project_id'] != '0':
                try:
                    project_obj = Project.objects.get(id=int(n['project_id']))
                    project = Project.objects.filter(
                        title=project_obj.title
                    ).first()
                except (Project.DoesNotExist, ValueError):
                    self.stdout.write(
                        self.style.WARNING(
                            f"Проект с id={n['project_id']} "
                            f"не найден для новости '{n['title']}'"
                        )
                    )

            news_obj, is_created = News.objects.get_or_create(
                title=n['title'],
                date=n['date'] if n['date'] else date(2024, 1, 1),
                defaults={
                    'summary': n['short_text'],
                    'full_text': n['detail_text'],
                    'photo': clean_media_path(n['photo']),
                    'detail_page_type': (
                        News.DetailPageChoices.CREATE
                        if n['detail_text']
                        else News.DetailPageChoices.NONE
                    ),
                    'detail_page_link': n['ext_url'],
                    'video_url': n['video'],
                    'project': project,
                },
            )
            if is_created:
                created += 1
                if n['section_name']:
                    direction, _ = Direction.objects.get_or_create(
                        name=n['section_name']
                    )
                    news_obj.directions.add(direction)
                gallery_paths = split_gallery(n['gallery'])
                for img_path in gallery_paths:
                    GalleryImage.objects.create(
                        news=news_obj,
                        image=img_path,
                        name=img_path.split('/')[-1],
                    )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Создана новость: {news_obj.title}, фото: "
                        f"{n['photo']}, галерея: {len(gallery_paths)}"
                    )
                )
            else:
                skipped += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Импорт завершён: создано {created}, пропущено {skipped}'
            )
        )

    def extract_news(self, sql_dump):
        """Извлекает и парсит все новости из SQL-дампа (таблица `news`)."""
        insert_regex = re.compile(
            r'INSERT INTO `news`.*?VALUES\s*(.+);', re.DOTALL
        )
        match = insert_regex.search(sql_dump)
        if not match:
            raise ValueError('Не найден блок INSERT INTO `news`')
        values_section = match.group(1)
        tuples = parse_sql_tuples(values_section)
        news = []
        for t in tuples:
            if len(t) < 15:
                continue
            news.append(
                {
                    'title': t[2],
                    'short_text': t[3],
                    'detail_text': t[4],
                    'photo': t[5],
                    'date': parse_date(t[6]) if t[6] else None,
                    'gallery': t[7],
                    'video': t[8],
                    'ext_url': t[9],
                    'section_name': t[10],
                    'project_id': t[14],
                }
            )
        return news
