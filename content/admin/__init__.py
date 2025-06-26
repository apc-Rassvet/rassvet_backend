"""Пакет админских классов для приложения content."""

from .about_us_video import AboutUsVideoAdmin
from .employees import EmployeeAdmin
from .gratitudes import GratitudeAdmin
from .mission import MissionAdmin
from .news import DirectionAdmin, NewsAdmin
from .partners import PartnersAdmin
from .projects import ProgramsProjectsAdmin, ProjectAdmin
from .reviews import ReviewAdmin
from .targeted_fundraisings import TargetedFundraisingAdmin
from .report import ChapterAdmin
from .vacancies import VacancyAdmin
from .training_and_internships import TrainingAndInternshipsAdmin

__all__ = [
    'AboutUsVideoAdmin',
    'DirectionAdmin',
    'EmployeeAdmin',
    'GratitudeAdmin',
    'MissionAdmin',
    'NewsAdmin',
    'PartnersAdmin',
    'ProjectAdmin',
    'ProgramsProjectsAdmin',
    'ReviewAdmin',
    'TargetedFundraisingAdmin',
    'ChapterAdmin',
    'VacancyAdmin',
    'TrainingAndInternshipsAdmin',
]
