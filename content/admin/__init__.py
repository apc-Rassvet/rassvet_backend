"""Пакет админских классов для приложения content."""

from .about_us_video import AboutUsVideoAdmin
from .coaching import CoachingAdmin
from .employees import EmployeeAdmin
from .gratitudes import GratitudeAdmin
from .mission import MissionAdmin
from .news import DirectionAdmin, NewsAdmin
from .partners import PartnersAdmin
from .projects import ProgramsProjectsAdmin, ProjectAdmin
from .report import ChapterAdmin
from .reviews import ReviewAdmin
from .supervisors import SupervisorAdmin
from .targeted_fundraisings import TargetedFundraisingAdmin
from .vacancies import VacancyAdmin

__all__ = [
    'AboutUsVideoAdmin',
    'ChapterAdmin',
    'CoachingAdmin',
    'DirectionAdmin',
    'EmployeeAdmin',
    'GratitudeAdmin',
    'MissionAdmin',
    'NewsAdmin',
    'SupervisorAdmin',
    'PartnersAdmin',
    'ProjectAdmin',
    'ProgramsProjectsAdmin',
    'ReviewAdmin',
    'TargetedFundraisingAdmin',
    'VacancyAdmin',
]
