# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls')),  # User management
    path('departments/', include('apps.departments.urls')),  # Departments app
    path('minutes/', include('apps.minutes.urls')),  # Minutes app
    path('analytics/', include('apps.analytics.urls')),  # Analytics app
    path("approval-chain/", include("approval_chain.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

