"""
URL configuration for BiblioParque project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Aplicaciones.Visitas.views import registro_visita, registro_usuario, usuario_guardado, principal, inicio_secion, validacion_correo, correo_contrasenas
from Aplicaciones.Visitas.views import eleccion_visita, recuperar, datos_usuario, visita_guardada, datos_actualizados, funcionamiento, eleccion_recupera, datos_acceso, modificar_acceso
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",principal, name="principal"),
    path("visita/", registro_visita, name="registro_visita"),
    path("usuario/", registro_usuario, name="registro_usuario"),
    path("guardado/", usuario_guardado, name="usuario_guardado"),
    path('eleccion/', eleccion_visita, name='eleccion'),
    path('secion/',inicio_secion, name='inicio_secion'),
    path('recuperar/',recuperar, name='recuperar'),
    path('datos_usuario/', datos_usuario, name='datos_usuario'),
    path('visita_guardada/', visita_guardada, name='visita_guardada'),
    path('datos_actualizados/', datos_actualizados, name='datos_actualizados'),
    path('funcionamiento/', funcionamiento, name='funcionamiento'),
    path('eleccion_recupera/',  eleccion_recupera, name='eleccion_recupera'),
    path('validacion_correo/', validacion_correo, name='validacion_correo'),
    path('datos_acceso/', datos_acceso, name='datos_acceso'),
    path('correo_contraseñas/',correo_contrasenas,name='correo_contrasenas'),
    path('modificar_acceso/',modificar_acceso,name='modificar_acceso'),

]
