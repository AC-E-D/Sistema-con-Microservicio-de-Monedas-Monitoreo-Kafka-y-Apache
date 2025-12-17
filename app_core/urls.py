# app_core/urls.py
from django.urls import path
from . import views
from .views_monitor import (
    monitor_dashboard,
    monitor_data,
    monitor_monedas,   # 👈 NUEVO
)

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # CRUD
    path('productos/', views.productos_view, name='productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),

    # Monedas
    path('monedas/', views.consulta_monedas, name='monedas'),

    # Dashboard de monitoreo
    path('monitor/', monitor_dashboard, name='monitor'),
    path('monitor/data/', monitor_data, name='monitor_data'),

    # 👉 NUEVO: datos de monedas para gráficos (microservicio)
    path('monitor/monedas/', monitor_monedas, name='monitor_monedas'),
]
