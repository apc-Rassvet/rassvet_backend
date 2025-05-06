from django.apps import AppConfig
from django.db.models.signals import post_migrate

# from content.models.supervisors import Page


class ContentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'content'
