from rest_framework.pagination import PageNumberPagination

from .constants import (
    GRATITUDE_PAGE_SIZE,
    GRATITUDE_MAX_PAGES,
    REVIEW_PAGE_SIZE,
    REVIEW_MAX_PAGES,
)


class GratitudePagination(PageNumberPagination):
    """Пагинация для благодарностей в разделе 'О нас'."""

    page_size = GRATITUDE_PAGE_SIZE
    page_size_query_param = 'page_size'
    max_page_size = GRATITUDE_MAX_PAGES


class ReviewPagination(PageNumberPagination):
    """Пагинация для отзывов страница 'О нас'."""

    page_size = REVIEW_PAGE_SIZE
    max_page_size = REVIEW_MAX_PAGES
