from collections import OrderedDict

from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)
from rest_framework.response import Response


class NewsLimitOffsetPagination(LimitOffsetPagination):
    """Пагинация для новостей."""

    default_limit = 6


class LiteraturePageNumberPagination(PageNumberPagination):
    """Пагинация для литературы."""

    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """Генерирует ответ с пагинацией и дополнительными полями."""
        return Response(
            OrderedDict(
                [
                    ('count', self.page.paginator.count),
                    ('total_pages', self.page.paginator.num_pages),
                    ('current_page', self.page.number),
                    ('page_size', self.get_page_size(self.request)),
                    ('next', self.get_next_link()),
                    ('previous', self.get_previous_link()),
                    ('results', data),
                ]
            )
        )
