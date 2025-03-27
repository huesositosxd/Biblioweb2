from django.db import models
from django.utils.timezone import localtime
from django.utils import timezone

class RegistroVisita(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.PositiveIntegerField()
    sexo = models.CharField(max_length=1)
    colonia = models.CharField(max_length=100)
    discapacidad = models.BooleanField()
    actividad = models.CharField(max_length=20)
    fecha_hora = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.nombre}"
