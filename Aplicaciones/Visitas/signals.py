from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import RegistroUsuario
from .tasks import eliminar_usuario_si_no_verificado

@receiver(post_save, sender=RegistroUsuario)
def enviar_codigo_hex(sender, instance, created, **kwargs):
    if created:
        asunto = "Tu código de Validacion"
        mensaje = (
            f"Hola {instance.nombre},\n\n"
            f"Gracias por registrarte. Tu código único de validación es: {instance.codigo_hex}\n\n"
             "Utiliza este código para completar tu registro como usuario.\n"
             "Si tú no solicitaste este registro, puedes ignorar este mensaje sin problema.\n\n"
             "¡Gracias y bienvenido!"
        )
        destinatario = [instance.correo_electronico]

        send_mail(
            asunto,
            mensaje,
            settings.EMAIL_HOST_USER,  # Asegúrate de tenerlo configurado
            destinatario,
            fail_silently=False,
        )