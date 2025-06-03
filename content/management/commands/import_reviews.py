"""Django management команда для импорта данных отзывов."""

from typing import Any

from content.management.config import MODEL_CONFIG
from content.management.utils import ImporterBase
from content.models import Review


class Command(ImporterBase):
    """Команда Django для импорта данных отзывов."""

    help = 'Импорт благодарностей из TXT-файла'
    model_class = Review
    file_path = 'reviews.txt'
    model_config: Any = MODEL_CONFIG[model_class]
