from django.urls import path, include


urlpatterns = [
    path('', include('content.api.urls'))
]
