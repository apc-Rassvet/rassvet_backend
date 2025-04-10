from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from drf_spectacular.utils import extend_schema


@extend_schema(exclude=True)
class HiddenSchemaView(SpectacularAPIView):
    pass


urlpatterns = [
    path(
        'admin/password_reset/',
        auth_views.PasswordResetView.as_view(),
        name='admin_password_reset',
    ),
    path(
        'admin/password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        'admin/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'admin/reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
    path('admin/', admin.site.urls),
    path(
        'api/schema/',
        HiddenSchemaView.as_view(),
        name='schema',
    ),
    path(
        'api/docs/swagger-ui/',
        SpectacularSwaggerView.as_view(
            url_name='schema',
        ),
        name='swagger-ui',
    ),
    path(
        'api/docs/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
    path('api/', include('content.urls')),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
