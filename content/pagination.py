from rest_framework.pagination import LimitOffsetPagination


class NewsLimitOffsetPagination(LimitOffsetPagination):
    """Пагинация для новостей."""

    default_limit = 6
