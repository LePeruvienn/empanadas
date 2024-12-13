from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path( 'admin/', admin.site.urls),
    path( '', include('empanadas.urls')),
    path( '', include('comptes.urls')),
    path( '', include('paniers.urls')),
    path( 'stats/', include('stats.urls') ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
