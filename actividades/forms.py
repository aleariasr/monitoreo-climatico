from django import forms
from .models import Actividad

class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = [
            'nombre_actividad',
            'ubicacion',
            'latitud',
            'longitud',
            'fecha_actividad',
        ]

        widgets = {
            'nombre_actividad' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Ej: Caminata'
            }),

            'ubicacion' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Ej: Grecia, Alajuela'
            }),

            'latitud': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'placeholder': 'Ej: 10.0733'
            }),

            'longitud': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'placeholder': 'Ej: -84.3120'
            }),

            'fecha_actividad': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }