from django.db import models

class RegistroVisita(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.PositiveIntegerField()
    sexo = models.CharField(max_length=1)
    colonia = models.CharField(max_length=100)
    discapacidad = models.CharField(max_length=2)
    actividad = models.CharField(max_length=20)
    fecha_hora = models.DateTimeField()
    fecha_nacimiento = models.DateField(null=True, blank=True)
    estado_nacimiento = models.CharField(max_length=30, default='desconocido')
    aviso_privacidad = models.BooleanField(default=False)

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
    aviso_privacidad = models.BooleanField(default=False)

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
    fecha_visita = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Visita de {self.usuario.nombre} el {self.fecha_visita}'

class Recuperar(models.Model):
    correo=models.EmailField()
    curp = models.CharField(max_length=18)
    contrasena = models.CharField(max_length=128)

    def __str__(self):
        return self.nombre
