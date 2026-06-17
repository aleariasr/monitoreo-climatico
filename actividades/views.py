# Estudiante: Alejandro Arias Rojas
# Herramienta de IA utilizada: ChatGPT
# La IA fue utilizada para apoyar la estructura del CRUD, consumo de API REST
# y conexión con el procedimiento almacenado en MySQL.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import connection
from django.utils import timezone
import requests

from .models import Actividad
from .forms import ActividadForm


def lista_actividades(request):
    actividades = Actividad.objects.all().order_by('-id')
    return render(request, 'actividades/lista.html', {
        'actividades': actividades
    })


def crear_actividad(request):
    if request.method == 'POST':
        form = ActividadForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Actividad registrada correctamente.')
            return redirect('lista_actividades')
    else:
        form = ActividadForm()

    return render(request, 'actividades/formulario.html', {
        'form': form,
        'titulo': 'Registrar actividad'
    })


def editar_actividad(request, actividad_id):
    actividad = get_object_or_404(Actividad, id=actividad_id)

    if request.method == 'POST':
        form = ActividadForm(request.POST, instance=actividad)

        if form.is_valid():
            form.save()
            messages.success(request, 'Actividad modificada correctamente.')
            return redirect('lista_actividades')
    else:
        form = ActividadForm(instance=actividad)

    return render(request, 'actividades/formulario.html', {
        'form': form,
        'titulo': 'Editar actividad'
    })


def eliminar_actividad(request, actividad_id):
    actividad = get_object_or_404(Actividad, id=actividad_id)

    if request.method == 'POST':
        actividad.delete()
        messages.success(request, 'Actividad eliminada correctamente.')
        return redirect('lista_actividades')

    return render(request, 'actividades/confirmar_eliminar.html', {
        'actividad': actividad
    })


def consultar_clima(request, actividad_id):
    actividad = get_object_or_404(Actividad, id=actividad_id)

    url = (
        'https://api.open-meteo.com/v1/forecast'
        f'?latitude={actividad.latitud}'
        f'&longitude={actividad.longitud}'
        '&current=temperature_2m,wind_speed_10m,precipitation'
    )

    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()
        datos = respuesta.json()

        clima_actual = datos.get('current', {})

        temperatura = clima_actual.get('temperature_2m')
        velocidad_viento = clima_actual.get('wind_speed_10m')
        precipitacion = clima_actual.get('precipitation')

        if temperatura is None or velocidad_viento is None or precipitacion is None:
            messages.error(request, 'La API no devolvió todos los datos climáticos requeridos.')
            return redirect('lista_actividades')

        with connection.cursor() as cursor:
            cursor.callproc(
                'sp_calcular_riesgo_climatico',
                [temperatura, velocidad_viento, precipitacion]
            )
            resultado = cursor.fetchone()

        nivel_riesgo = resultado[0] if resultado else 'BAJO'

        actividad.temperatura = temperatura
        actividad.velocidad_viento = velocidad_viento
        actividad.precipitacion = precipitacion
        actividad.nivel_riesgo = nivel_riesgo
        actividad.fecha_consulta = timezone.now()
        actividad.save()

        messages.success(request, 'Clima consultado correctamente.')

    except requests.RequestException:
        messages.error(request, 'No se pudo consultar la API Open-Meteo.')

    except Exception as error:
        messages.error(request, f'Ocurrió un error: {error}')

    return redirect('lista_actividades')