from django.apps import AppConfig


class VisitasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Aplicaciones.Visitas'

    def ready(self):
        import Aplicaciones.Visitas.signals
