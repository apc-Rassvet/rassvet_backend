"""Django management команда для импорта данных сборов средств."""

from typing import Any

from content.management.config import MODEL_CONFIG
from content.management.utils import ImporterBase
from content.models import (
    FundraisingPhoto,
    FundraisingTextBlock,
    TargetedFundraising,
)


class Command(ImporterBase):
    """Команда Django для импорта данных целевых сборов средств."""

    help = 'Импорт благодарностей из TXT-файла'
    model_class = TargetedFundraising
    file_path = 'fundraisings.txt'
    model_config: Any = MODEL_CONFIG[model_class]

    def post_process_instance(self, instance, row, row_num):
        """Выполняет дополнительную обработку после создания целевого сбора."""
        self._process_photos(instance, row)
        self._process_text_blocks(instance, row)
        return True

    def _process_photos(self, instance, row):
        """Обрабатывает фотографии для целевого сбора."""
        for i in range(1, 4):
            if photo_path := row.get(f'photo{i}'):
                self._create_photo(instance, photo_path, i)

    def _create_photo(self, instance, path, position):
        """Создает и сохраняет фотографию для целевого сбора."""
        photo = FundraisingPhoto(
            title=f'Фото {position} для {instance.title}',
            fundraising=instance,
            position=position,
        )
        photo.save()
        if self.save_file_to_model(photo, path, 'image'):
            self.stdout.write(
                f"Загружено фото {position} для сбора '{instance.title}'"
            )

    def _process_text_blocks(self, instance, row):
        """Обрабатывает текстовые блоки для целевого сбора."""
        text_blocks = [
            FundraisingTextBlock(
                fundraising=instance, content=row[f'text{i}'], position=i
            )
            for i in range(1, 4)
            if row.get(f'text{i}')
        ]

        if text_blocks:
            FundraisingTextBlock.objects.bulk_create(text_blocks)
            self.stdout.write(
                f'Создано {len(text_blocks)} '
                f'текстовых блоков для сбора "{instance.title}"'
            )
