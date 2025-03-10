from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('usuarios.urls')),
    path('produtos/', include('produtos.urls')),
    path('admin/', admin.site.urls),
    path('pedido/', include('pedidos.urls')),
    path("__reload__", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
