"""Пакет админских классов для приложения content."""

from .about_us_video import AboutUsVideoAdmin
from .coaching import CoachingAdmin
from .employees import EmployeeAdmin
from .gratitudes import GratitudeAdmin
from .knowledge_base import ArticleAdmin, ChapterKnowledgeBaseAdmin
from .mission import MissionAdmin
from .literatures import Literature
from .news import DirectionAdmin, NewsAdmin
from .partners import PartnersAdmin
from .projects import ProgramsProjectsAdmin, ProjectAdmin
from .report import ChapterAdmin
from .reviews import ReviewAdmin
from .supervisors import SupervisorAdmin
from .targeted_fundraisings import TargetedFundraisingAdmin
from .useful_links import ChapterUsefulLinksAdmin
from .vacancies import VacancyAdmin
from .training_and_internships import TrainingAndInternshipsAdmin

__all__ = [
    'AboutUsVideoAdmin',
    'ArticleAdmin',
    'ChapterAdmin',
    'ChapterUsefulLinksAdmin',
    'CoachingAdmin',
    'ChapterKnowledgeBaseAdmin',
    'DirectionAdmin',
    'EmployeeAdmin',
    'GratitudeAdmin',
    'Literature',
    'MissionAdmin',
    'NewsAdmin',
    'SupervisorAdmin',
    'PartnersAdmin',
    'ProjectAdmin',
    'ProgramsProjectsAdmin',
    'ReviewAdmin',
    'TargetedFundraisingAdmin',
    'VacancyAdmin',
    'TrainingAndInternshipsAdmin',
]
