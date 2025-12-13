from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView

from drf_spectacular.views import SpectacularAPIView, SpectacularJSONAPIView

urlpatterns = [
    path('admin/', admin.site.urls),

    # App principal
    path('app_core/', include('app_core.urls')),
    path('', RedirectView.as_view(url='/app_core/login/', permanent=False)),

    # API interna
    path('api/', include('api.urls')),

    # FORZAR JSON (ReDoc lo necesita)
    path('api/schema/', SpectacularJSONAPIView.as_view(), name='schema'),

    # Swagger local (plantilla)
    path(
        'swagger/',
        TemplateView.as_view(template_name='app_core/swagger.html'),
        name='swagger-ui'
    ),

    # ReDoc local
    path(
        'redoc/',
        TemplateView.as_view(template_name='app_core/redoc.html'),
        name='redoc-ui'
    ),
]

# MANEJADORES GLOBALES DE ERRORES (Django los usará cuando DEBUG = False)
handler400 = "app_core.views.error_400"
handler403 = "app_core.views.error_403"
handler404 = "app_core.views.error_404"
handler500 = "app_core.views.error_500"
