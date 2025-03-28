from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('article/', include('article.urls')),
    path('auth/', include('article.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
