"""Django management команда для импорта данных благодарностей."""

from typing import Any

from content.management.config import MODEL_CONFIG
from content.management.utils import ImporterBase
from content.models import Gratitude


class Command(ImporterBase):
    """Команда Django для импорта данных благодарностей."""

    help = 'Импорт благодарностей из TXT-файла'
    model_class = Gratitude
    file_path = 'gratitudes.txt'
    model_config: Any = MODEL_CONFIG[model_class]

    def post_process_instance(self, instance, row, row_num):
        """Выполняет дополнительную обработку после создания благодарности."""
        if self.save_file_to_model(instance, row['file'], 'file'):
            self.stdout.write(f"Благодарность '{instance.title}' создана")
            return True
        return False
