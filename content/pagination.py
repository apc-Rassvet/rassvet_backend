from rest_framework.pagination import LimitOffsetPagination


class NewsLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 6
