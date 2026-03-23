"""
URL configuration for tas_school project.
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .admin import admin_site
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('', include('accounts.urls')),  # Set the root URL to point to accounts app
    path('admin/', admin_site.urls),

    # JWT endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('auth/', include('accounts.urls')),
    path('accounts/', include('accounts.urls')),
    path('courses/', include('courses.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 