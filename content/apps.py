from django.apps import AppConfig
from django.db.models.signals import post_migrate

# from content.models.supervisors import Page


class ContentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'content'

    def ready(self):
        post_migrate.connect(create_pages, sender=self)

def create_pages(sender, **kwargs):
    from content.models.supervisors import Page
    Page.objects.get_or_create(name='aba-therapy')
    Page.objects.get_or_create(name='adaptive-physical-culture')
    Page.objects.get_or_create(name='creative-workshops')
    Page.objects.get_or_create(name='resource-classes')
    Page.objects.get_or_create(name='children-leisure')

# class SupervisorsConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'supervisors'

#     def ready(self):
#         post_migrate.connect(create_pages, sender=self)

# def create_pages(sender, **kwargs):
#     Page.objects.get_or_create(name='aba-therapy')
#     Page.objects.get_or_create(name='adaptive-physical-culture')
#     Page.objects.get_or_create(name='creative-workshops')
#     Page.objects.get_or_create(name='resource-classes')
#     Page.objects.get_or_create(name='children-leisure')

