"""Маршруты API для приложения forms.

Этот модуль определяет маршруты для версии API v1 относящиеся к формам:
- FeedbackFormView: форма обратной связи.
"""

from django.urls import path

from .views import FeedbackFormView

urlpatterns = [
    path('feedback/', FeedbackFormView.as_view(), name='feedback_form'),
]
