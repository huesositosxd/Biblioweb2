from django.shortcuts import render, redirect
from django.utils.timezone import make_aware, is_naive
import pytz
from datetime import datetime
from .models import RegistroVisita

def registro_visita(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        edad = request.POST.get("edad")
        sexo = request.POST.get("sexo")
        colonia = request.POST.get("colonia")
        discapacidad = request.POST.get("discapacidad") == "si"
        actividad = request.POST.get("actividad")
        fecha_hora_str = request.POST.get("fecha_hora")  # Fecha recibida del formulario

        # Zona horaria de Monterrey
        zona_horaria = pytz.timezone('America/Monterrey')

        if fecha_hora_str:  # Si viene del formulario, convertirla
            fecha_hora_dt = datetime.strptime(fecha_hora_str, "%d/%m/%Y %H:%M:%S")
            if is_naive(fecha_hora_dt):  # Si no tiene zona horaria, se la agregamos
                fecha_hora = make_aware(fecha_hora_dt, timezone=zona_horaria)
            else:  # Si ya tiene zona horaria, la usamos directamente
                fecha_hora = fecha_hora_dt
        else:  # Si no, usar la fecha y hora actual de Monterrey sin make_aware
            fecha_hora = datetime.now(zona_horaria)

        if nombre and edad and sexo and colonia and actividad:
            RegistroVisita.objects.create(
                nombre=nombre,
                edad=int(edad),
                sexo=sexo,
                colonia=colonia,
                discapacidad=discapacidad,
                actividad=actividad,
                fecha_hora=fecha_hora  # Ahora sí se almacena correctamente
            )
            return render(request, "registros.html")

    return render(request, "registros.html")
