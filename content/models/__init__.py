"""Пакет моделей приложения content.

Содержит все модели данных, используемые для управления контентом:
- Благодарности
- Отзывы
- Партнёры
- Видео "О нас"
- Адресные сборы и связанные сущности
- Сотрудники и их документы

Все модели регистрируются здесь для обеспечения корректного импорта и миграций.
"""

from .about_us_video import AboutUsVideo
from .employees import Document, Employee, TypeDocument
from .gratitudes import Gratitude
from .mission import Mission
from .partners import Partner
from .projects import ProgramsProjects, Project, ProjectPhoto
from .reviews import Review
from .targeted_fundraisings import (
    FundraisingPhoto,
    FundraisingTextBlock,
    TargetedFundraising,
)

__all__ = [
    'AboutUsVideo',
    'Document',
    'Employee',
    'FundraisingPhoto',
    'FundraisingTextBlock',
    'Gratitude',
    'Mission',
    'Partner',
    'ProgramsProjects',
    'Project',
    'ProjectPhoto',
    'Review',
    'TargetedFundraising',
    'TypeDocument',
]
