"""Конфигурация ASGI для проекта 'АПЦ Рассвет'.

Этот модуль обеспечивает точку входа для ASGI-совместимых веб-серверов
для обслуживания проекта.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rassvet.settings')

application = get_asgi_application()
