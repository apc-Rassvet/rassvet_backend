"""Django command для автоматизированного запуска всех команд импорта.

Эта команда последовательно запускает заданный список команд импорта,
обрабатывает исключения и выводит информацию о результатах выполнения каждой.
Используется для упрощения процесса импорта данных в систему.

Использование:
    python manage.py import_all_data

Команда запускает следующие импорты:
- import_employees: Импорт данных о сотрудниках
- import_fundraisings: Импорт данных о сборах
- import_video: Импорт видео 'О нас'
- import_gratitudes: Импорт благодарностей
- import_partners: Импорт данных о партнерах
- import_reviews: Импорт отзывов

В случае возникновения ошибки при выполнении какой-либо команды,
будет выведено сообщение об ошибке, но выполнение остальных команд продолжится.
"""

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Команда для запуска всех команд импорта."""

    help = 'Запускает все команды импорта данных'

    def handle(self, *args, **kwargs):
        """Запускает команду."""
        self.stdout.write('Начинаем выполнение всех команд импорта...')
        commands = [
            'import_employees',
            'import_fundraisings',
            'import_video',
            'import_gratitudes',
            'import_partners',
            'import_reviews',
        ]
        for command in commands:
            self.stdout.write(f'Запуск команды: {command}')
            try:
                call_command(command)
                self.stdout.write(
                    self.style.SUCCESS(f'Команда {command} выполнена успешно.')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Ошибка при выполнении команды {command}: {str(e)}'
                    )
                )
        self.stdout.write(self.style.SUCCESS('Все команды импорта выполнены.'))
