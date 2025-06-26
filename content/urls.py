"""Конфигурация URL для проекта.

Этот модуль определяет URL-шаблоны верхнего уровня для проекта.
"""

from django.urls import include, path
from drf_spectacular.utils import extend_schema
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


@extend_schema(exclude=True)
class HiddenSchemaView(SpectacularAPIView):
    """Класс представления схемы API с исключением из документации.

    Этот класс наследуется от SpectacularAPIView и использует декоратор
    extend_schema с параметром exclude=True для скрытия этого эндпоинта
    из генерируемой документации API.
    """

    pass


urlpatterns = [
    path(
        'schema/',
        HiddenSchemaView.as_view(),
        name='schema',
    ),
    path(
        'docs/swagger-ui/',
        SpectacularSwaggerView.as_view(
            url_name='schema',
        ),
        name='swagger-ui',
    ),
    path(
        'docs/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
    path('', include('content.api.urls')),
]
