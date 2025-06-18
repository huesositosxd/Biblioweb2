from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import localtime, make_aware, is_naive
from datetime import datetime
from datetime import datetime
import pytz
from .models import RegistroVisita, RegistroUsuario, Visitausuario, Recuperar
from django.db import models
import secrets
from django.core.mail import send_mail
from django.conf import settings

def registro_visita(request): 
    """
    Vista para registrar visitas anónimas.
    Se guarda la fecha y hora usando la zona America/Monterrey.
    """
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
        parque = request.POST.get("parque")
        discapacidad_es = request.POST.get("discapacidad_es")

        # Zona horaria fija para Saltillo/Monterrey
        zona_horaria = pytz.timezone('America/Monterrey')

        if fecha_hora_str:
            fecha_hora_dt = datetime.strptime(fecha_hora_str, "%d/%m/%Y %H:%M:%S")
            if is_naive(fecha_hora_dt):
                fecha_hora = zona_horaria.localize(fecha_hora_dt)
            else:
                fecha_hora = fecha_hora_dt
        else:
            fecha_hora = datetime.now()

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
                parque=parque,
                discapacidad_es =discapacidad_es
            )
            return render(request, "registro_visitas_com.html")

    return render(request, "registro_visitas_com.html")


def registro_usuario(request):
    """
    Vista para registrar usuarios con cuenta.
    """
    errores = {}
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        fecha_nacimiento_str = request.POST.get("fecha_nacimiento")
        edad = request.POST.get("edad")
        sexo = request.POST.get("sexo")
        colonia = request.POST.get("colonia")
        discapacidad = request.POST.get("discapacidad") == "No"
        CURP = request.POST.get("CURP")
        estado_nacimiento = request.POST.get("estado_nacimiento")
        correo_electronico = request.POST.get("correo")
        contraseña = request.POST.get("password")
        aviso_valor = request.POST.get("aviso_privacidad")
        aviso_privacidad = aviso_valor in ["on", "si", "true", "True"]

        # Convertir fecha de nacimiento
        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            errores["fecha_nacimiento"] = "Fecha inválida"
            fecha_nacimiento = None

        # Validar CURP solo si cambió
        if CURP != request.POST.get("CURP_original"):
            if RegistroUsuario.objects.filter(CURP=CURP).exists():
                errores["CURP"] = "Esta CURP ya está registrada."

        # Validar correo solo si cambió
        if correo_electronico != request.POST.get("correo_original"):
            if RegistroUsuario.objects.filter(correo_electronico=correo_electronico).exists():
                errores["correo"] = "Este correo ya está registrado."

        if not aviso_privacidad:
            errores["aviso_privacidad"] = "Debes aceptar los términos."

        if not errores and nombre and edad and sexo and colonia and CURP and estado_nacimiento and correo_electronico and contraseña:
            usuario = RegistroUsuario.objects.create(
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
            request.session['usuario_id'] = usuario.id
            request.session['correo'] = usuario.correo_electronico
            return redirect("validacion_correo")

    return render(request, "registro_usuario.html", {"errores": errores})


def inicio_secion(request):
    """
    Vista para iniciar sesión y registrar visita de usuario autenticado.
    La fecha de visita se graba con zona America/Monterrey (hora local).
    """
    errores = {}
    if request.method == 'POST':
        dato = request.POST.get('coreo_curp')  # Puede ser CURP o correo
        actividad = request.POST.get('actividad')
        parque = request.POST.get('parque')

        usuario = RegistroUsuario.objects.filter(CURP=dato).first()
        if not usuario:
            usuario = RegistroUsuario.objects.filter(correo_electronico=dato).first()

        if usuario:
            fecha_visita_local = datetime.now()

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
                actividad=actividad,
                parque=parque,
                fecha_visita=fecha_visita_local
            )
            return redirect('visita_guardada')
        else:
            messages.error(request, 'Usuario no encontrado. Verifica CURP o correo.')

    return render(request, 'inicio_secion.html', {"errores": errores})

def recuperar(request):
    """
    Vista para recuperar datos de usuario (por correo y CURP o contraseña).
    """
    if request.method == 'POST':
        correo_electronico = request.POST.get('correo')
        curp_contraseña = request.POST.get('curp_contraseña')

        usuario = RegistroUsuario.objects.filter(
            correo_electronico=correo_electronico
        ).filter(
            models.Q(CURP=curp_contraseña) | models.Q(contraseña=curp_contraseña)
        ).first()

        if usuario:
            request.session['usuario_id'] = usuario.id
            return render(request, 'datos_usuario.html', {'usuario': usuario})

        return render(request, 'recuperar.html', {
            'error': 'Los datos no coinciden con nuestros registros.'
        })

    return render(request, 'recuperar.html')


def datos_usuario(request):
    """
    Vista para mostrar y actualizar los datos del usuario autenticado (sesión).
    """
    errores = {}

    if not request.session.get('usuario_id'):
        return redirect('inicio_secion')  # Redirigir si no hay usuario en sesión

    usuario = get_object_or_404(RegistroUsuario, id=request.session['usuario_id'])

    if request.method == 'POST':
        nuevo_nombre = request.POST.get('nombre')
        fecha_nacimiento_str = request.POST.get('fecha_nacimiento')
        nueva_edad = request.POST.get('edad')
        nuevo_sexo = request.POST.get('sexo')
        nueva_colonia = request.POST.get('colonia')
        nueva_discapacidad = request.POST.get('discapacidad')
        nuevo_curp = request.POST.get('CURP')
        nuevo_estado_nacimiento = request.POST.get('estado_nacimiento')

        try:
            fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            errores["fecha_nacimiento"] = "Fecha inválida"
            fecha_nacimiento = None

        if not errores:
            usuario.nombre = nuevo_nombre
            usuario.fecha_nacimiento = fecha_nacimiento
            usuario.edad = int(nueva_edad)
            usuario.sexo = nuevo_sexo
            usuario.colonia = nueva_colonia
            usuario.discapacidad = nueva_discapacidad
            usuario.CURP = nuevo_curp
            usuario.estado_nacimiento = nuevo_estado_nacimiento
            usuario.save()
            return redirect('datos_actualizados')

    return render(request, 'datos_usuario.html', {'usuario': usuario, 'errores': errores})


def usuario_guardado(request):
    """
    Vista simple que muestra confirmación de usuario guardado.
    """
    return render(request, "usuario_guardado.html")


def principal(request):
    """
    Vista principal (landing page).
    """
    return render(request, "principal.html")


def eleccion_visita(request):
    """
    Vista para elegir tipo de visita (anónima o usuario).
    """
    return render(request, "eleccion_visita.html")


def visita_guardada(request):
    """
    Vista simple que muestra confirmación de visita guardada.
    """
    return render(request, "visita_guardada.html")


def datos_actualizados(request):
    """
    Vista simple que muestra confirmación de que datos fueron actualizados.
    """
    return render(request, "datos_actualizados.html")


def funcionamiento(request):
    """
    Vista de información sobre el funcionamiento de la aplicación.
    """
    return render(request, "funcionamiento.html")

def  eleccion_recupera (request):
    return render (request,'eleccion_recupera.html')

def validacion_correo(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('principal')

    try:
        usuario = RegistroUsuario.objects.get(id=usuario_id)
    except RegistroUsuario.DoesNotExist:
        return redirect('registro_usuario')

    if request.method == 'POST':
        codigo_ingresado = request.POST.get('codigo', '').strip().upper()
        clave_intentos = f'intentos_{usuario.id}'
        intentos = request.session.get(clave_intentos, 0)

        if usuario.codigo_hex == codigo_ingresado:
            usuario.verificado = True

            # Cambiar código solo si fue verificado exitosamente
            usuario.codigo_hex = secrets.token_hex(3).upper()

            usuario.save()

            # Limpiar la sesión
            request.session.pop(clave_intentos, None)
            request.session.pop('usuario_id', None)
            return redirect('usuario_guardado')

        else:
            # Aumentar intentos
            intentos += 1
            request.session[clave_intentos] = intentos

            if intentos >= 3:
                # Eliminar cuenta después de 3 intentos fallidos
                usuario.delete()
                request.session.pop(clave_intentos, None)
                request.session.pop('usuario_id', None)

                messages.error(request, 'Demasiados intentos fallidos. Tu cuenta ha sido eliminada.')
                return redirect('registro_usuario')

            messages.warning(request, f'Código incorrecto. Intento {intentos} de 3.')

    return render(request, 'validacion_correo.html', {'correo': usuario.correo_electronico})

def validar_datos_acceso(request):
    return render(request, 'validar_datos_acceso.html')

def datos_acceso(request):
    errores = {}

    if request.method == 'POST':
        dato = request.POST.get('correo')  # Nombre del campo en el formulario

        # Buscar usuario por correo electrónico
        usuario = RegistroUsuario.objects.filter(correo_electronico=dato).first()

        if usuario:
            # Generar y guardar nuevo código de verificación
            nuevo_codigo = secrets.token_hex(3).upper()
            usuario.codigo_hex = nuevo_codigo
            usuario.save()

            # Guardar en sesión
            request.session['usuario_id'] = usuario.id
            request.session['correo'] = usuario.correo_electronico

            # Enviar correo con nuevo código
            asunto = "Código de verificación para acceso"
            mensaje = (
                f"Hola {usuario.nombre},\n\n"
                f"Tu nuevo código de verificación es: {nuevo_codigo}\n\n"
                "Por favor ingrésalo en la página para continuar.\n"
                "Si no solicitaste este código, puedes ignorar este mensaje."
            )

            send_mail(
                asunto,
                mensaje,
                settings.EMAIL_HOST_USER,
                [usuario.correo_electronico],
                fail_silently=False
            )

            return redirect('correo_contrasenas')
        else:
            messages.error(request, 'Correo no encontrado. Verifica que esté bien escrito.')

    return render(request, 'datos_acceso.html', {"errores": errores})

def correo_contrasenas(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('principal')

    try:
        usuario = RegistroUsuario.objects.get(id=usuario_id)
    except RegistroUsuario.DoesNotExist:
        return redirect('datos_acceso')

    mostrar_alerta = False  # Para indicar si es el tercer intento fallido

    if request.method == 'POST':
        codigo_ingresado = request.POST.get('codigo', '').strip().upper()
        clave_intentos = f'intentos_acceso_{usuario.id}'
        intentos = request.session.get(clave_intentos, 0)

        if usuario.codigo_hex == codigo_ingresado:
            usuario.codigo_hex = secrets.token_hex(3).upper()
            usuario.save()
            request.session.pop(clave_intentos, None)
            return redirect('modificar_acceso')
        else:
            intentos += 1
            request.session[clave_intentos] = intentos

            if intentos >= 3:
                mostrar_alerta = True  # Señalamos que se debe mostrar la alerta JS
                request.session.pop(clave_intentos, None)

            else:
                messages.warning(request, f'Código incorrecto. Intento {intentos} de 3.')

    return render(request, 'correo_contrasenas.html', {
        'correo': usuario.correo_electronico,
        'mostrar_alerta': mostrar_alerta
    })

def modificar_acceso(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('principal')

    usuario = get_object_or_404(RegistroUsuario, id=usuario_id)

    if request.method == 'POST':
        nueva_pass    = request.POST.get('password', '').strip()
        confirma_pass = request.POST.get('confirm_password', '').strip()

        # Validaciones básicas
        if len(nueva_pass) < 6 or nueva_pass != confirma_pass:
            # El JS del template se encargará de mostrar alertas, 
            # dejamos aquí solo un mensaje general por si JS está desactivado.
            messages.error(request, "Revisa las contraseñas; deben coincidir y tener al menos 6 caracteres.")
            return render(request, 'modificar_acceso.html', {
                'correo': usuario.correo_electronico
            })

        # Guardar nueva contraseña y limpiar sesión
        usuario.contraseña = nueva_pass
        usuario.save()
        request.session.pop('usuario_id', None)

        messages.success(request, "Contraseña actualizada correctamente. Inicia sesión de nuevo.")
        return redirect('inicio_secion')

    # GET → renderizar con el correo prellenado
    return render(request, 'modificar_acceso.html', {
        'correo': usuario.correo_electronico
    })