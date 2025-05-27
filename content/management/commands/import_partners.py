"""Django management команда для импорта данных партнеров."""

from typing import Any

from content.management.config import MODEL_CONFIG
from content.management.utils import ImporterBase
from content.models import Partner


class Command(ImporterBase):
    """Команда Django для импорта данных партнеров."""

    help = 'Импорт благодарностей из TXT-файла'
    model_class = Partner
    file_path = 'partners.txt'
    model_config: Any = MODEL_CONFIG[model_class]

    def post_process_instance(self, instance, row, row_num):
        """Выполняет дополнительную обработку после создания партнера."""
        if self.save_file_to_model(instance, row['logo'], 'logo'):
            self.stdout.write(f"Партнёр '{instance.name}' создан")
            return True
        return False
