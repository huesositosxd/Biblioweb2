# myproject/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establecer el módulo de configuración predeterminado de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BiblioParque.settings')

app = Celery('BiblioParque')

# Usar una cadena para que no sea necesario un objeto de configuración de tipo módulo.
# El string aquí debe coincidir con el nombre del proyecto.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Cargar tareas de todos los módulos de tareas en INSTALLED_APPS.
app.autodiscover_tasks()
