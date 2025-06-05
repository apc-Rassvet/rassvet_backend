"""Django management команда для импорта проектов из дампа SQL."""

import os
import pandas as pd

from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from django.core.files import File

from content.models import Project, ProgramsProjects, Partner, ProjectPhoto


class Command(BaseCommand):
    help = 'Импортирует проекты из Excel в базу данных'

    def handle(self, *args, **options):
        excel_path = 'data/projects.xlsx'
        images_dir = 'media_images/'
        self.stdout.write(self.style.WARNING(
            'Удаляем все проекты и связанные фотографии...'))
        ProjectPhoto.objects.all().delete()
        Project.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(
            'Все проекты и фотографии удалены.'))
        STATUS_MAP = {
            'действующий': 'active',
            'завершённый': 'completed',
            'завершенный': 'completed',
        }
        df = pd.read_excel(excel_path)
        for i, row in df.iterrows():
            row_num = i + 2  # для удобства (с учётом заголовка)
            if pd.isna(row['title']):
                continue
            program_title = (
                row['program'] if pd.notna(row['program']) else None
            )
            program = None
            if program_title:
                program, created = ProgramsProjects.objects.get_or_create(
                    title=program_title.strip()
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"[{row_num}] Программа '{program_title}' "
                            "была создана."
                        )
                    )
            partner_title = row['source_financing'] if pd.notna(
                row['source_financing']) else None
            partner = None
            if partner_title:
                partner = Partner.objects.filter(
                    name=partner_title.strip()).first()
                if not partner:
                    self.stdout.write(self.style.WARNING(
                        f"[{row_num}] Партнёр '{partner_title}' не найден. "
                        "Проект будет добавлен без него."))
            status = STATUS_MAP.get(
                str(row['status']).strip().lower(), 'active'
            )
            logo_file = None
            if pd.notna(row['logo']) and row['logo'].strip():
                logo_path = os.path.join(
                    images_dir, os.path.basename(row['logo'].strip())
                )
                if os.path.isfile(logo_path):
                    logo_file = File(open(logo_path, 'rb'))
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"[{row_num}] Логотип '{logo_path}' не найден. "
                            'Проект будет без логотипа.'
                        )
                    )
            project = Project(
                title=row['title'],
                status=status,
                project_start=parse_date(str(row['project_start']))
                if pd.notna(row['project_start'])
                else None,
                project_end=parse_date(str(row['project_end']))
                if pd.notna(row['project_end'])
                else None,
                source_financing=partner,
                program=program,
                project_goal=row.get('project_goal', ''),
                project_tasks=row.get('project_tasks', ''),
                project_description=row.get('project_description', ''),
                achieved_results=row.get('achieved_results', ''),
            )
            if logo_file:
                project.logo.save(
                    os.path.basename(row['logo'].strip()),
                    logo_file,
                    save=False,
                )
            project.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"[{row_num}] Проект '{project.title}' добавлен."
                )
            )
            if pd.notna(row.get('photo')):
                for img_path in str(row['photo']).split('\n'):
                    img_path = img_path.strip()
                    if not img_path:
                        continue
                    photo_path = os.path.join(
                        images_dir, os.path.basename(img_path)
                    )
                    if os.path.isfile(photo_path):
                        with open(photo_path, 'rb') as img_f:
                            photo_file = File(img_f)
                            photo_obj = ProjectPhoto(project=project)
                            photo_obj.image.save(
                                os.path.basename(img_path),
                                photo_file,
                                save=True,
                            )
                            self.stdout.write(
                                f'    + Фото: {photo_obj.image.url}'
                            )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"    + Фото '{photo_path}' не найдено. "
                                'Пропущено.'
                            )
                        )
        self.stdout.write(self.style.SUCCESS('Импорт завершён!'))
