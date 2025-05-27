from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import make_aware, is_naive
from datetime import datetime
from .models import RegistroVisita, RegistroUsuario, Visitausuario, Recuperar
from django.contrib import messages
import pytz
from django.db import models

def registro_visita(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        edad = request.POST.get("edad")
        sexo = request.POST.get("sexo")
        colonia = request.POST.get("colonia")
        discapacidad_valor = request.POST.get("discapacidad")
        discapacidad = discapacidad_valor == "si"
        actividad = request.POST.get("actividad")
        aviso_valor = request.POST.get("aviso_privacidad")
        aviso_privacidad = aviso_valor in ["on", "si", "true", "True"]
        estado_nacimiento = request.POST.get("estado_nacimiento")

        fecha_hora_str = request.POST.get("fecha_hora")
        fecha_nacimiento_str = request.POST.get("fecha_nacimiento")

        zona_horaria = pytz.timezone('America/Monterrey')

        if fecha_hora_str:
            fecha_hora_dt = datetime.strptime(fecha_hora_str, "%d/%m/%Y %H:%M:%S")
            fecha_hora = make_aware(fecha_hora_dt, timezone=zona_horaria) if is_naive(fecha_hora_dt) else fecha_hora_dt
        else:
            fecha_hora = datetime.now(zona_horaria)

        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            fecha_nacimiento = None

        if nombre and edad and sexo and colonia and actividad:
            RegistroVisita.objects.create(
                nombre=nombre,
                edad=int(edad),
                sexo=sexo,
                colonia=colonia,
                discapacidad=discapacidad,
                actividad=actividad,
                fecha_hora=fecha_hora,
                aviso_privacidad=aviso_privacidad,
                estado_nacimiento=estado_nacimiento,
                fecha_nacimiento=fecha_nacimiento
            )
            return render(request, "registro_visitas_com.html")

    return render(request, "registro_visitas_com.html")


def registro_usuario(request):
    errores = {}
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        fecha_nacimiento_str = request.POST.get("fecha_nacimiento")
        edad = request.POST.get("edad")
        sexo = request.POST.get("sexo")
        colonia = request.POST.get("colonia")
        discapacidad = request.POST.get("discapacidad")=='No'
        CURP = request.POST.get("CURP")
        estado_nacimiento = request.POST.get("estado_nacimiento")
        correo_electronico = request.POST.get("correo")
        contraseña = request.POST.get("password")
        aviso_valor = request.POST.get("aviso_privacidad")
        aviso_privacidad = aviso_valor in ["on", "si", "true", "True"]

        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            errores["fecha_nacimiento"] = "Fecha inválida"

        if CURP != request.POST.get("CURP_original"):  # Usamos un campo oculto para verificar si ha cambiado
            if RegistroUsuario.objects.filter(CURP=CURP).exists():
                errores["CURP"] = "Esta CURP ya está registrada."

        # Verificar correo solo si ha cambiado
        if correo_electronico != request.POST.get("correo_original"):  # Usamos un campo oculto para verificar si ha cambiado
            if RegistroUsuario.objects.filter(correo_electronico=correo_electronico).exists():
                errores["correo"] = "Este correo ya está registrado."


        if not aviso_privacidad:
            errores["aviso_privacidad"] = "Debes aceptar los términos."

        if not errores and nombre and edad and sexo and colonia and CURP and estado_nacimiento and correo_electronico and contraseña:
            RegistroUsuario.objects.create(
                nombre=nombre,
                fecha_nacimiento=fecha_nacimiento,
                edad=int(edad),
                sexo=sexo,
                colonia=colonia,
                discapacidad=discapacidad,
                CURP=CURP,
                estado_nacimiento=estado_nacimiento,
                correo_electronico=correo_electronico,
                contraseña=contraseña,
                aviso_privacidad=aviso_privacidad
            )
            return redirect("usuario_guardado")

    return render(request, "registro_usuario.html", {"errores": errores})


def inicio_secion(request):
    if request.method == 'POST':
        dato = request.POST.get('coreo_curp')  # cuidado con el nombre
        actividad = request.POST.get('actividad')

        usuario = RegistroUsuario.objects.filter(CURP=dato).first()
        if not usuario:
            usuario = RegistroUsuario.objects.filter(correo_electronico=dato).first()

        if usuario:
            Visitausuario.objects.create(
                usuario=usuario,
                nombre=usuario.nombre,
                fecha_nacimiento=usuario.fecha_nacimiento,
                edad=usuario.edad,
                sexo=usuario.sexo,
                colonia=usuario.colonia,
                discapacidad=usuario.discapacidad,
                CURP=usuario.CURP,
                estado_nacimiento=usuario.estado_nacimiento,
                actividad=actividad
            )
            return redirect('visita_guardada')
        else:
            messages.error(request, 'Usuario no encontrado. Verifica CURP o correo.')

    return render(request, 'inicio_secion.html')


def recuperar(request):
    if request.method=='POST':
        correo_electronico=request.POST.get('correo')
        curp_contraseña = request.POST.get('curp_contraseña')

        #Pregunta si existen los datos
        usuario = RegistroUsuario.objects.filter(
            correo_electronico=correo_electronico
        ).filter(
            models.Q(CURP=curp_contraseña) | models.Q(contraseña=curp_contraseña)
        ).first()

        #redirigue si existen
        if usuario:
            request.session['usuario_id'] = usuario.id
            return render(request, 'datos_usuario.html', {'usuario': usuario})

        return render(request, 'recuperar.html', {
            'error': 'Los datos no coinciden con nuestros registros.'
        })

    return render(request, 'recuperar.html')


def datos_usuario(request):
    errores = {}

    if not request.session.get('usuario_id'):
        return redirect('inicio_secion')  # Redirigir si no hay usuario en la sesión

    usuario = get_object_or_404(RegistroUsuario, id=request.session['usuario_id'])

    if request.method == 'POST':
        print("DEBUG datos_usuario POST:", request.POST)
        nuevo_nombre = request.POST.get('nombre')
        fecha_nacimiento_str = request.POST.get('fecha_nacimiento')
        nueva_edad = request.POST.get('edad')
        nuevo_sexo = request.POST.get('sexo')
        nueva_colonia = request.POST.get('colonia')
        nueva_discapacidad = request.POST.get('discapacidad')
        nuevo_curp = request.POST.get('CURP')
        nuevo_estado_nacimiento = request.POST.get('estado_nacimiento')
        nuevo_correo = request.POST.get('correo')
        nueva_contraseña = request.POST.get('password')
        aviso_valor = request.POST.get("aviso_privacidad")
        aviso_privacidad = aviso_valor in ["on", "si", "true", "True"]

        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            errores["fecha_nacimiento"] = "Fecha inválida"

        if not aviso_privacidad:
            errores["aviso_privacidad"] = "Debes aceptar los términos."

        if not errores:
            usuario.nombre = nuevo_nombre
            usuario.fecha_nacimiento = fecha_nacimiento
            usuario.edad = int(nueva_edad)
            usuario.sexo = nuevo_sexo
            usuario.colonia = nueva_colonia
            usuario.discapacidad = nueva_discapacidad
            usuario.CURP = nuevo_curp
            usuario.estado_nacimiento = nuevo_estado_nacimiento
            usuario.correo_electronico = nuevo_correo
            usuario.contraseña = nueva_contraseña
            usuario.aviso_privacidad = aviso_privacidad

            usuario.save()
            return redirect('datos_actualizados')

    return render(request, 'datos_usuario.html', {'usuario': usuario, 'errores': errores})

def usuario_guardado(request):
    return render(request, "usuario_guardado.html")


def principal(request):
    return render(request, "principal.html")


def eleccion_visita(request):
    return render(request, "eleccion_visita.html")

def visita_guardada(request):
    return render(request,"visita_guardada.html")

def datos_actualizados(request):
    return render (request,"datos_actualizados.html")

def funcionamiento(request):
    return render(request,"funcionamiento.html")