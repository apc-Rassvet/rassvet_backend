import os
import csv

from django.core.management.base import BaseCommand

from content.models import (
    AboutUsVideo,
    Gratitude,
    Review,
    Partner,
    TargetedFundraising,
    FundraisingPhoto,
    FundraisingTextBlock,
)
from content.models.targeted_fundraisings import FundraisingStatus


class Command(BaseCommand):
    help = 'Импорт данных из TXT-файлов в базу данных'

    def handle(self, *args, **kwargs):
        base_path = 'data/'

        with open(
            os.path.join(base_path, 'video.txt'), 'r', encoding='utf-8'
        ) as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                AboutUsVideo.objects.update_or_create(
                    title=row['Заголовок Alt'],
                    defaults={'url': row['URL (ссылка)']},
                )

        with open(
            os.path.join(base_path, 'gratitudes.txt'), 'r', encoding='utf-8'
        ) as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                if row['Файл']:
                    Gratitude.objects.update_or_create(
                        title=row.get('Заголовок* (А)', 'Без названия'),
                        defaults={
                            'file': row['Файл'],
                            'order': row['Порядок'],
                            'is_active': True,
                        },
                    )

        with open(
            os.path.join(base_path, 'reviews.txt'), 'r', encoding='utf-8'
        ) as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                Review.objects.update_or_create(
                    author_name=row['Автор (заголовок)'],
                    defaults={
                        'content': row['Текст'],
                        'order': row['Порядок'],
                        'is_active': row['Активен'] == 'да',
                    },
                )

        with open(
            os.path.join(base_path, 'partners.txt'), 'r', encoding='utf-8'
        ) as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                Partner.objects.update_or_create(
                    name=row['Название'],
                    defaults={
                        'logo': row['Логотип'],
                        'description': row['Описание'],
                        'order': 0,
                    },
                )

        with open(
            os.path.join(base_path, 'fundraisings.txt'), 'r', encoding='utf-8'
        ) as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                status = (
                    FundraisingStatus.ACTIVE
                    if row['Статус'] == 'Актуальный'
                    else FundraisingStatus.COMPLETED
                )
                fundraising, created = (
                    TargetedFundraising.objects.update_or_create(
                        title=row['Заголовок'],
                        defaults={
                            'short_description': row['Краткое описание'],
                            'fundraising_link': row['Ссылка на сбор*'],
                            'status': status,
                            'order': row['Порядок'],
                        },
                    )
                )

                for i in range(1, 4):
                    photo_field = f'Фото{i}*' if i > 1 else f'Фото{i}'
                    if row.get(photo_field):
                        FundraisingPhoto.objects.update_or_create(
                            fundraising=fundraising,
                            position=i,
                            defaults={'image': row[photo_field]},
                        )

                for i in range(1, 4):
                    text_field = f'Текст{i}*' if i > 1 else f'Текст{i}'
                    if row.get(text_field):
                        FundraisingTextBlock.objects.update_or_create(
                            fundraising=fundraising,
                            position=i,
                            defaults={'content': row[text_field]},
                        )

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))
