"""Константы приложения content."""

TITLE_LENGTH = 255
"""Максимальная длина заголовка."""

CHAR_FIELD_LENGTH = 255
"""Максимальная длина поля CharField."""

ORDER_DEFAULT = 0
"""Значение по умолчанию для порядка отображения элементов."""

IMAGE_CONTENT_TYPES = [
    'jpg',
    'jpeg',
    'png',
    'webp',
]
"""Формат загрузки файлов для ImageField."""

VIDEO_CONTENT_TYPES = [
    'avi',
    'mp4',
]
"""Формат загрузки файлов для FileField video."""

FILE_CONTENT_TYPES = ['pdf']
"""Формат загрузки файлов для FileField."""

EMPTY_VALUE_DISPLAY = '-пусто-'
"""Отображение пустого поля."""
