"""Django management команда для импорта проектов из дампа SQL."""

from django.core.management.base import BaseCommand

from content.management.utils import extract_projects_from_sql
from content.models import Project, ProgramsProjects, ProjectsStatus


class Command(BaseCommand):
    """Django management-команда для импорта проектов из дампа SQL."""

    help = 'Импортирует проекты из дампа SQL'

    def handle(self, *args, **options):
        """Основной метод команды."""
        sql_file = 'data/rassvet_dump.sql'
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_dump = f.read()
        projects = extract_projects_from_sql(sql_dump)
        program, _ = ProgramsProjects.objects.get_or_create(
            title='Основная программа'
        )

        created, skipped = 0, 0
        for p in projects:
            obj, is_created = Project.objects.get_or_create(
                title=p['name'],
                defaults={
                    'project_description': p['description'] or '',
                    'status': ProjectsStatus.ACTIVE,
                    'project_rassvet': False,
                    'program': program,
                    'logo': 'projects/default.png',
                    'project_goal': '',
                    'project_tasks': '',
                    'achieved_results': '',
                },
            )
            if is_created:
                self.stdout.write(
                    self.style.SUCCESS(f'Создан проект: {obj.title}')
                )
                created += 1
            else:
                skipped += 1
        self.stdout.write(
            self.style.SUCCESS(
                f'Импорт завершён: создано {created}, пропущено {skipped}'
            )
        )
