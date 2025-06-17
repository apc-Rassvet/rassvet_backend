"""Пакет админских классов для приложения content."""

from .about_us_video import AboutUsVideoAdmin
from .coaching import CoachingAdmin
from .employees import EmployeeAdmin
from .gratitudes import GratitudeAdmin
from .mission import MissionAdmin
from .news import DirectionAdmin, NewsAdmin
from .partners import PartnersAdmin
from .projects import ProgramsProjectsAdmin, ProjectAdmin
from .reviews import ReviewAdmin
from .targeted_fundraisings import TargetedFundraisingAdmin
from .report import ChapterAdmin

__all__ = [
    'AboutUsVideoAdmin',
    'CoachingAdmin',
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
]
