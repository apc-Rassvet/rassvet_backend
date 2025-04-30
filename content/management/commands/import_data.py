import os
import csv
import pandas as pd

from django.core.files import File
from django.core.management.base import BaseCommand

from content.models import (
    AboutUsVideo,
    Gratitude,
    Employee,
    Review,
    Partner,
    TargetedFundraising,
    FundraisingPhoto,
    FundraisingTextBlock,
    TypeDocument,
    Document,
)
from content.models.targeted_fundraisings import FundraisingStatus


MEDIA_PATH = 'media_data'


class Command(BaseCommand):
    help = 'Импорт данных из TXT-файлов в базу данных'

    def handle(self, *args, **kwargs):
        base_path = 'data/'
        gratitude_count = Gratitude.objects.all().count()
        Gratitude.objects.all().delete()
        self.stdout.write(f'Удалено {gratitude_count} старых благодарностей')
        review_count = Review.objects.all().count()
        Review.objects.all().delete()
        self.stdout.write(f'Удалено {review_count} старых отзывов')
        partner_count = Partner.objects.all().count()
        Partner.objects.all().delete()
        self.stdout.write(f'Удалено {partner_count} старых партнёров')
        fundraising_count = TargetedFundraising.objects.all().count()
        TargetedFundraising.objects.all().delete()
        self.stdout.write(f'Удалено {fundraising_count} старых сборов')
        employee_count = Employee.objects.all().count()
        Employee.objects.all().delete()
        self.stdout.write(f'Удалено {employee_count} старых сотрудников')
        with open(
            os.path.join(base_path, 'video.txt'), 'r', encoding='utf-8'
        ) as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                AboutUsVideo.objects.update_or_create(
                    title=row['title'],
                    url=row['url'],
                )

        with open(
            os.path.join(base_path, 'gratitudes.txt'), 'r', encoding='utf-8'
        ) as f:
            reader = csv.DictReader(f, delimiter='\t')
            gratitude_count = 0
            for row_num, row in enumerate(reader, 1):
                if not row.get('file'):
                    self.stdout.write(
                        self.style.WARNING(
                            f'Пропущена строка {row_num}: отсутствует файл'
                        )
                    )
                    continue
                file_path = row['file'].lstrip('\\')
                absolute_path = MEDIA_PATH + file_path

                try:
                    title = row.get('title') or f'Благодарность #{row_num}'
                    gratitude = Gratitude(
                        title=title,
                        order=row.get('order', 0),
                        is_active=True,
                    )

                    with open(absolute_path, 'rb') as file_obj:
                        gratitude.file.save(
                            os.path.basename(file_path),
                            File(file_obj),
                            save=True,
                        )
                    gratitude_count += 1
                    self.stdout.write(f"Благодарность '{title}' создана")
                except FileNotFoundError:
                    self.stdout.write(
                        self.style.ERROR(f'Файл не найден: {absolute_path}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Ошибка при импорте {file_path}: {str(e)}'
                        )
                    )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Импортировано {gratitude_count} благодарностей'
                )
            )

        with open(
            os.path.join(base_path, 'reviews.txt'), 'r', encoding='utf-8'
        ) as f:
            reader = csv.DictReader(f, delimiter='\t')
            review_count = 0
            for row in reader:
                review, created = Review.objects.update_or_create(
                    author_name=row['author_name'],
                    defaults={
                        'content': row['content'],
                        'order': row['order'],
                        'is_active': row['is_active'] == 'да',
                    },
                )
                review_count += 1
                status = 'создан' if created else 'обновлен'
                self.stdout.write(f"Отзыв от '{row['author_name']}' {status}")
            self.stdout.write(
                self.style.SUCCESS(f'Импортировано {review_count} отзывов')
            )

        with open(
            os.path.join(base_path, 'partners.txt'), 'r', encoding='utf-8'
        ) as f:
            reader = csv.DictReader(f, delimiter='\t')
            partner_count = 0
            for row_num, row in enumerate(reader, 1):
                if not row.get('logo'):
                    continue
                file_path = row['logo'].lstrip('\\')
                absolute_path = MEDIA_PATH + file_path
                try:
                    name = row.get('name') or f'Партнёр #{row_num}'
                    partner = Partner(
                        name=name,
                        description=row.get('description'),
                        order=row.get('order', 0),
                    )

                    with open(absolute_path, 'rb') as file_obj:
                        partner.logo.save(
                            os.path.basename(file_path),
                            File(file_obj),
                            save=True,
                        )
                    partner_count += 1
                    self.stdout.write(f"Партнёр '{name}' создан")
                except FileNotFoundError:
                    self.stdout.write(
                        self.style.ERROR(f'Файл не найден: {absolute_path}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Ошибка при импорте {file_path}: {str(e)}'
                        )
                    )
            self.stdout.write(
                self.style.SUCCESS(f'Импортировано {partner_count} партнёров')
            )

        with open(
            os.path.join(base_path, 'fundraisings.txt'), 'r', encoding='utf-8'
        ) as f:
            reader = csv.DictReader(f, delimiter='\t')
            fundraising_count = 0
            for row in reader:
                status = (
                    FundraisingStatus.ACTIVE
                    if row['status'].lower() == 'актуальный'
                    else FundraisingStatus.COMPLETED
                )
                fundraising = TargetedFundraising.objects.create(
                    title=row['title'],
                    short_description=row['short_description'],
                    fundraising_link=row.get('fundraising_link', ''),
                    status=status,
                    order=int(row.get('order', 0)),
                )
                fundraising_count += 1
                self.stdout.write(
                    f"Создан сбор '{fundraising.title}' со статусом '{status}'"
                )
                for i in range(1, 4):
                    photo_field = f'photo{i}'
                    if photo_field in row and row[photo_field]:
                        photo_path = row[photo_field].lstrip('/')
                        absolute_path = os.path.join(MEDIA_PATH, photo_path)
                        try:
                            photo = FundraisingPhoto(
                                title=f'Фото {i} для {fundraising.title}',
                                fundraising=fundraising,
                                position=i,
                            )
                            with open(absolute_path, 'rb') as file_obj:
                                photo.image.save(
                                    os.path.basename(photo_path),
                                    File(file_obj),
                                    save=True,
                                )
                                self.stdout.write(
                                    f"Загружено фото {i} для сбора '"
                                    f"{fundraising.title}'"
                                )
                        except FileNotFoundError:
                            self.stdout.write(
                                self.style.ERROR(
                                    f'Файл не найден: {absolute_path}'
                                )
                            )
                        except Exception as e:
                            self.stdout.write(
                                self.style.ERROR(
                                    f'Ошибка при импорте фото {photo_path}: '
                                    f'{str(e)}'
                                )
                            )
                for i in range(1, 4):
                    text_field = f'text{i}'
                    if text_field in row and row[text_field]:
                        try:
                            FundraisingTextBlock.objects.create(
                                fundraising=fundraising,
                                content=row[text_field],
                                position=i,
                            )
                            self.stdout.write(
                                f'Создан текстовый блок {i} для сбора '
                                f"'{fundraising.title}'"
                            )
                        except Exception as e:
                            self.stdout.write(
                                self.style.ERROR(
                                    f'Ошибка при создании текстового блока '
                                    f"{i} для сбора '{fundraising.title}': "
                                    f'{str(e)}'
                                )
                            )
            self.stdout.write(
                self.style.SUCCESS(f'Импортировано {fundraising_count} сборов')
            )

        excel_file = 'data/employees.xlsx'

        try:
            if not os.path.exists(excel_file):
                self.stdout.write(
                    self.style.ERROR(f'Файл не найден: {excel_file}')
                )
                return
            df = pd.read_excel(excel_file, dtype=str)
            df = df.fillna('')
            employee_count = 0
            document_count = 0
            current_employee = None
            for index, row in df.iterrows():
                name = row.get('Имя', '')
                if name:
                    employee, created = Employee.objects.update_or_create(
                        name=name,
                        defaults={
                            'main_specialities': row.get(
                                'Специальности на странице Команда', ''
                            ),
                            'specialities': row.get(
                                'Специальности подробная', ''
                            ),
                            'order': (
                                int(row.get('Порядок', 999))
                                if row.get('Порядок')
                                and str(row.get('Порядок')).isdigit()
                                else 999
                            ),
                            'education': row.get('Образование', ''),
                            'additional_education': row.get(
                                'Доп. Образование', ''
                            ),
                            'trainings': row.get('Тренинги', ''),
                            'interviews': row.get('Интервью', ''),
                            'specialists_register': row.get(
                                'Реестр специалистов', ''
                            ),
                        },
                    )
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f'Создан сотрудник: {name}')
                        )
                    else:
                        self.stdout.write(
                            self.style.SUCCESS(f'Обновлен сотрудник: {name}')
                        )
                    current_employee = employee
                    employee_count += 1
                    photo_url = (
                        MEDIA_PATH + row.get('Фотография', '')
                    ).strip()
                    if (
                        photo_url
                        and isinstance(photo_url, str)
                        and not photo_url.isspace()
                    ):
                        photo_filename = os.path.basename(photo_url)
                        try:
                            if os.path.exists(photo_url):
                                with open(photo_url, 'rb') as f:
                                    employee.image.save(
                                        photo_filename,
                                        File(f),
                                        save=True,
                                    )
                                    self.stdout.write(
                                        self.style.SUCCESS(
                                            f'Загружено фото: {photo_filename}'
                                        )
                                    )
                            else:
                                self.stdout.write(
                                    self.style.WARNING(
                                        f'Файл не найден: {photo_url}'
                                    )
                                )
                        except Exception as e:
                            self.stdout.write(
                                self.style.ERROR(
                                    f'Ошибка при обработке изображения: {e}'
                                )
                            )
                file_path = (
                    MEDIA_PATH + row.get('Файл сертификата', '').strip()
                )
                cert_name = row.get('Название сертификата', '')
                cert_type = row.get('Тип сертификата', '')
                if file_path and cert_type and current_employee:
                    if not cert_name:
                        cert_name = os.path.basename(file_path).split('.')[0]
                    if cert_type == 'лента':
                        document, created = Document.objects.update_or_create(
                            name=cert_name,
                            employee=current_employee,
                            on_main_page=True,
                        )
                    else:
                        doc_type, created = TypeDocument.objects.get_or_create(
                            name=cert_type
                        )
                        if created:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f'Создан тип документа: {cert_type}'
                                )
                            )
                        document, created = Document.objects.update_or_create(
                            name=cert_name,
                            employee=current_employee,
                            type=doc_type,
                            defaults={'on_main_page': False},
                        )
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Создан документ: {cert_name} для '
                                f'{current_employee.name}'
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Обновлен документ: {cert_name} для '
                                f'{current_employee.name}'
                            )
                        )
                    document_count += 1
                    if created or not document.file:
                        try:
                            if os.path.exists(file_path):
                                with open(file_path, 'rb') as f:
                                    document.file.save(
                                        os.path.basename(file_path),
                                        File(f),
                                        save=True,
                                    )
                                    self.stdout.write(
                                        self.style.SUCCESS(
                                            f'Загружен файл документа: '
                                            f'{os.path.basename(file_path)}'
                                        )
                                    )
                            else:
                                self.stdout.write(
                                    self.style.WARNING(
                                        f'Файл документа не найден: '
                                        f'{file_path}'
                                    )
                                )
                        except Exception as e:
                            self.stdout.write(
                                self.style.ERROR(
                                    f'Ошибка при обработке файла '
                                    f'документа: {e}'
                                )
                            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Импорт данных успешно завершен. Обработано сотрудников: '
                    f'{employee_count}, документов: {document_count}'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при импорте данных: {e}')
            )
        self.stdout.write(self.style.SUCCESS('Данные загружены!'))
