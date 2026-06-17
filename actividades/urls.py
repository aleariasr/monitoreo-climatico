from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_actividades, name='lista_actividades'),
    path('nuevo/', views.crear_actividad, name='crear_actividad'),
    path('editar/<int:actividad_id>/', views.editar_actividad, name='editar_actividad'),
    path('eliminar/<int:actividad_id>/', views.eliminar_actividad, name='eliminar_actividad'),
    path('consultar-clima/<int:actividad_id>/', views.consultar_clima, name='consultar_clima'),
]