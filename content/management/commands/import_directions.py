"""Django management команда для импорта данных направлений."""

from typing import Any

from content.management.config import MODEL_CONFIG
from content.management.utils import ImporterBase
from content.models import Direction


class Command(ImporterBase):
    """Команда Django для импорта данных направлений."""

    help = 'Импорт направлений из TXT-файла'
    model_class = Direction
    file_path = 'directions.txt'
    model_config: Any = MODEL_CONFIG[model_class]
