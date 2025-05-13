"""Пакет админских классов для приложения content."""

from .about_us_video import AboutUsVideoAdmin
from .employees import EmployeeAdmin
from .gratitudes import GratitudeAdmin
from .mission import MissionAdmin
from .partners import PartnersAdmin
from .projects import ProgramsProjectsAdmin, ProjectAdmin
from .reviews import ReviewAdmin
from .targeted_fundraisings import TargetedFundraisingAdmin

__all__ = [
    'AboutUsVideoAdmin',
    'EmployeeAdmin',
    'GratitudeAdmin',
    'MissionAdmin',
    'PartnersAdmin',
    'ProjectAdmin',
    'ProgramsProjectsAdmin',
    'ReviewAdmin',
    'TargetedFundraisingAdmin',
]
