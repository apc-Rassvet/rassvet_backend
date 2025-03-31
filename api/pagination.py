from rest_framework.pagination import PageNumberPagination
from rassvet import constants


class GratitudePagination(PageNumberPagination):
    """Пагинация для благодарностей в разделе 'О нас'."""

    page_size = constants.GRATITUDE_PAGE_SIZE
    page_size_query_param = 'page_size'
    max_page_size = constants.GRATITUDE_MAX_PAGES
