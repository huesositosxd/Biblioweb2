# Aplicaciones.TuApp.tasks.py
from celery import shared_task
from .models import RegistroUsuario

@shared_task
def eliminar_usuario_si_no_verificado(usuario_id):
    try:
        usuario = RegistroUsuario.objects.get(id=usuario_id)
        if not usuario.verificado:
            usuario.delete()
    except RegistroUsuario.DoesNotExist:
        pass
