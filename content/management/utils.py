"""Базовый класс команды импорта.

Этот модуль содержит класс ImporterBase, являющийся базовым
для всех Django-команд импорта контентных данных из CSV/TSV-файлов.

Конфигурация импорта задается атрибутами класса:
    model_class: Класс модели для импорта.
    file_path: Имя файла с данными.
    delimiter: Разделитель полей в файле.
    clear_before_import: Флаг очистки существующих записей перед импортом.
    model_config: Конфигурация полей модели для импорта.

Media файлы считываются из папки MEDIA_PATH, данные из папки DATA_PATH.
"""

import csv
import os

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import models

MEDIA_PATH = 'media_data'
DATA_PATH = 'data'


class ImporterBase(BaseCommand):
    """Базовый класс для всех импортеров."""

    model_class: models.Model
    file_path: str = ''
    delimiter = '\t'
    clear_before_import = True
    model_config: dict = {}

    def add_arguments(self, parser):
        """Добавляет аргументы для команды."""
        parser.add_argument(
            '--no-clear',
            action='store_true',
            help='Не удалять существующие записи перед импортом',
        )

    def handle(self, *args, **kwargs):
        """Основной метод команды.

        Выполняет валидацию, опциональную очистку данных,
        импорт записей и выводит результат.
        """
        self.validate_importer()
        if self.clear_before_import and not kwargs.get('no_clear'):
            self._clear_existing_data()
        success_count = self.import_data(*args, **kwargs)
        self.stdout.write(
            self.style.SUCCESS(
                f'Импорт завершен. Успешно импортировано: {success_count}'
            )
        )

    def validate_importer(self):
        """Проверяет корректность настройки импортёра."""
        if not self.model_class:
            raise ValueError('Не определён класс модели')
        if not self.file_path:
            raise ValueError('Не задан путь к файлу')
        if not self.model_config:
            raise ValueError('Не определена конфигурация модели')

    def import_data(self, *args, **kwargs) -> int:
        """Импортирует данные из CSV/TSV-файла."""
        data_path = self.get_data_path(self.file_path)
        return self._process_csv(data_path)

    def _process_csv(self, data_path: str) -> int:
        """Обрабатывает CSV/TSV-файл и создает записи."""
        success_count = 0
        with open(data_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=self.delimiter)
            for row_num, row in enumerate(reader, 1):
                if self._validate_row(row_num, row):
                    try:
                        instance = self.create_instance(row, row_num)
                        if self.post_process_instance(instance, row, row_num):
                            success_count += 1
                    except Exception as e:
                        self.handle_error(
                            f'Ошибка в строке {row_num}: {str(e)}'
                        )
        return success_count

    def handle_error(self, message: str, row_num: int | None = None):
        """Унифицированная обработка ошибок при импорте."""
        error_msg = (
            f'Ошибка в строке {row_num}: {message}' if row_num else message
        )
        self.stdout.write(self.style.ERROR(error_msg))

    def create_instance(self, row: dict, row_num: int) -> models.Model:
        """Создает экземпляр модели на основе строки данных."""
        config = self.model_config
        model_fields = {}
        for field, mapping in config['fields'].items():
            source_field = mapping.get('source', field)
            default = mapping.get('default')
            transform = mapping.get('transform')
            raw_value = row.get(source_field, default)
            value = default if str(raw_value).strip() == '' else raw_value
            if transform and value not in (None, ''):
                try:
                    value = transform(value, row, row_num)
                except Exception as e:
                    self.handle_error(
                        f'Ошибка преобразования поля {field}: {str(e)}',
                        row_num,
                    )
                    value = default
            model_fields[field] = value
        return self.model_class.objects.create(**model_fields)

    def post_process_instance(
        self, instance: models.Model, row: dict, row_num: int
    ) -> bool:
        """Дополнительная пост-обработка экземпляра после создания.

        Предназначен для переопределения в подклассах.
        """
        return True

    def _validate_row(self, row_num: int, row: dict) -> bool:
        """Проверяет наличие обязательных полей в строке."""
        config = self.model_config
        required_fields = config.get('required_fields', [])

        missing = [
            field
            for field in required_fields
            if field not in row or not row[field]
        ]
        if missing:
            self.stdout.write(
                self.style.WARNING(
                    f'Пропущена строка {row_num}: '
                    f'отсутствуют поля {", ".join(missing)}'
                )
            )
            return False
        return True

    def _clear_existing_data(self):
        """Удаляет все существующие записи модели."""
        if not self.model_class:
            return
        count, _ = self.model_class.objects.all().delete()
        self.stdout.write(
            f'Удалено {count} записей модели {self.model_class.__name__}'
        )

    def get_media_path(self, relative_path: str) -> str:
        """Возвращает абсолютный путь к файлу медиа."""
        if not relative_path:
            return ''
        return os.path.join(MEDIA_PATH, relative_path.lstrip('\\/'))

    def get_data_path(self, filename: str) -> str:
        """Возвращает абсолютный путь к файлу данных."""
        return os.path.join(DATA_PATH, filename)

    def save_file_to_model(
        self,
        instance: models.Model,
        file_path: str,
        field_name: str = 'file',
        filename: str | None = None,
    ) -> bool:
        """Сохраняет файл в поле модели."""
        if not file_path:
            return False
        abs_path = self.get_media_path(file_path)
        try:
            if not os.path.exists(abs_path):
                self.stdout.write(
                    self.style.ERROR(f'Файл не найден: {abs_path}')
                )
                return False
            if not filename:
                filename = os.path.basename(abs_path)
            with open(abs_path, 'rb') as file_obj:
                getattr(instance, field_name).save(
                    filename,
                    File(file_obj),
                    save=True,
                )
            self.stdout.write(
                f"Файл '{filename}' сохранен в поле {field_name}"
            )
            return True
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Ошибка при сохранении файла {abs_path}: {str(e)}'
                )
            )
            return False
