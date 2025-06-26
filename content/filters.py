"""Модуль фильтров для API."""

import django_filters

from django.utils import timezone

from .models import News


def get_max_year():
    """Возвращает максимальное значение года для фильтрации."""
    return timezone.now().year + 5


class NewsFilter(django_filters.FilterSet):
    """Фильтр новостей по диапазону годов и направлениям деятельности."""

    direction_slug = django_filters.CharFilter(
        field_name='directions__slug', lookup_expr='in'
    )

    year_from = django_filters.NumberFilter(
        field_name='date',
        lookup_expr='year__gte',
        min_value=1900,
        max_value=get_max_year,
    )
    year_to = django_filters.NumberFilter(
        field_name='date',
        lookup_expr='year__lte',
        min_value=1900,
        max_value=get_max_year,
    )

    class Meta:
        """Метаданные фильтра: настраивает модель и поля фильтрации."""

        model = News
        fields = ('year_from', 'year_to', 'project', 'direction_slug')
