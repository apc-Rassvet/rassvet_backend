"""Пакет моделей приложения content.

Содержит все модели данных, используемые для управления контентом:
- Благодарности
- Отзывы
- Партнёры
- Видео "О нас"
- Адресные сборы и связанные сущности
- Сотрудники и их документы
- Проекты
- Новости

Все модели регистрируются здесь для обеспечения корректного импорта и миграций.
"""

from .about_us_video import AboutUsVideo
from .employees import Document, Employee, TypeDocument
from .gratitudes import Gratitude
from .mission import Mission
from .news import Direction, GalleryImage, News
from .partners import Partner
from .projects import ProgramsProjects, Project, ProjectPhoto, ProjectsStatus
from .reviews import Review
from .targeted_fundraisings import (
    FundraisingPhoto,
    FundraisingTextBlock,
    TargetedFundraising,
)
from .report import Report, Chapter
from .vacancies import Vacancy
from .training_and_internships import (
    FormatStudy,
    ActionOnButton,
    TrainingAndInternships,
    TrainingAndInternshipsPhoto,
)

__all__ = [
    'AboutUsVideo',
    'Chapter',
    'Direction',
    'Document',
    'Employee',
    'FundraisingPhoto',
    'FundraisingTextBlock',
    'GalleryImage',
    'Gratitude',
    'Mission',
    'News',
    'Partner',
    'ProgramsProjects',
    'Project',
    'ProjectPhoto',
    'ProjectsStatus',
    'Report',
    'Review',
    'TargetedFundraising',
    'TypeDocument',
    'Vacancy',
    'FormatStudy',
    'ActionOnButton',
    'TrainingAndInternships',
    'TrainingAndInternshipsPhoto',
]
