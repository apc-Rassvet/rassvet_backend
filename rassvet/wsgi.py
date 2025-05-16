"""Конфигурация WSGI для проекта 'АПЦ Рассвет'.

Этот модуль обеспечивает запуск проекта Django через WSGI-совместимый
веб-сервер.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rassvet.settings')

application = get_wsgi_application()
