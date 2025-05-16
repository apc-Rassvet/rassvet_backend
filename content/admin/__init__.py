"""Пакет админских классов для приложения content."""

from .about_us_video import AboutUsVideoAdmin
from .employees import EmployeeAdmin
from .gratitudes import GratitudeAdmin
from .news import DirectionAdmin, NewsAdmin
from .partners import PartnersAdmin
from .reviews import ReviewAdmin
from .targeted_fundraisings import TargetedFundraisingAdmin

__all__ = [
    'AboutUsVideoAdmin',
    'DirectionAdmin',
    'EmployeeAdmin',
    'GratitudeAdmin',
    'NewsAdmin',
    'PartnersAdmin',
    'ReviewAdmin',
    'TargetedFundraisingAdmin',
]
