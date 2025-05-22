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
]
