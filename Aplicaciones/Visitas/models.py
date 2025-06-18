from django.db import models
import random

class RegistroVisita(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.PositiveIntegerField()
    sexo = models.CharField(max_length=1)
    colonia = models.CharField(max_length=100)
    discapacidad = models.CharField(max_length=2,default='Ninguno')
    discapacidad_es = models.CharField(max_length=70, default='Ninguna')
    actividad = models.CharField(max_length=20)
    fecha_hora = models.DateTimeField()
    estado_nacimiento = models.CharField(max_length=30)
    aviso_privacidad = models.BooleanField(default=False)
    parque = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre}, {self.fecha_hora}, {self.fecha_nacimiento}, {self.estado_nacimiento}"

class RegistroUsuario(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    edad = models.PositiveIntegerField()
    sexo = models.CharField(max_length=1)
    colonia = models.CharField(max_length=100)
    discapacidad = models.CharField(max_length=2, default='No')
    CURP = models.CharField(max_length=18, unique=True)
    estado_nacimiento = models.CharField(max_length=30, default='desconocido')
    correo_electronico = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=100)
    codigo_hex = models.CharField(max_length=5, unique=True, blank=True, null=True)
    aviso_privacidad = models.BooleanField(default=False)
    verificado = models.BooleanField(default=False)


    def generar_codigo_hex(self):
        for _ in range(10):  # Intenta 10 veces generar un código único
            codigo = f"{random.randint(0, 0xFFFFF):05X}"
            if not RegistroUsuario.objects.filter(codigo_hex=codigo).exists():
                return codigo
        raise ValueError("No se pudo generar un código HEX único tras 10 intentos.")

    def save(self, *args, **kwargs):
        if not self.codigo_hex:
            self.codigo_hex = self.generar_codigo_hex()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombre} - {self.fecha_nacimiento} - {self.edad} años - {self.sexo} - {self.estado_nacimiento}'

class Visitausuario(models.Model):
    usuario = models.ForeignKey(RegistroUsuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    edad = models.PositiveIntegerField()
    sexo = models.CharField(max_length=1)
    colonia = models.CharField(max_length=100)
    discapacidad = models.CharField(max_length=2, default='no')
    CURP = models.CharField(max_length=18)
    estado_nacimiento = models.CharField(max_length=30)
    actividad = models.CharField(max_length=50)
    fecha_visita = models.DateTimeField()
    parque = models.CharField(max_length=50,default='desconocido')
    def __str__(self):
        return f'Visita de {self.usuario.nombre} el {self.fecha_visita}'

class Recuperar(models.Model):
    correo=models.EmailField()
    curp = models.CharField(max_length=18)
    contrasena = models.CharField(max_length=128)

    def __str__(self):
        return self.nombre
