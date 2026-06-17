from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Actividad(models.Model):
    nombre_actividad = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=150)

    latitud = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90)
        ]
    )

    longitud = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180)
        ]
    )

    fecha_actividad = models.DateField()

    temperatura = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    velocidad_viento = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    precipitacion = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )

    nivel_riesgo = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )

    fecha_consulta = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nombre_actividad


