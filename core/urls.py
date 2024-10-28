from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .views import HomeView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('users/', include('apps.users.urls')),
    path('tasks/', include('apps.tasks.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)