from django.db import models
from django.contrib.auth.models import User


class Profesor(models.Model):
    idProfesor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido1 = models.CharField(max_length=50)
    apellido2 = models.CharField(max_length=50)
    correo = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    esAdmin = models.BooleanField(default=False)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.nombre}"

class Asignatura (models.Model):
    idAsignatura = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

class Cursos (models.Model):
    idCurso = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length = 50)

    def __str__(self):
        return f"{self.nombre}"

class Aulas (models.Model):
    idAula = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length = 50)

class Dias (models.Model):
    idDia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length = 50)

class FranjaHoraria(models.Model):
    idFranjaHoraria = models.AutoField(primary_key=True)
    numeroFranja = models.IntegerField()
    descripcion = models.CharField(max_length = 50)
    esRecreo = models.BooleanField(default=False)
    horaInicio = models.TimeField(null=True, blank=True)


    def __str__(self):
        return f"{self.descripcion}"

class Horario(models.Model):
    idHorario = models.AutoField(primary_key=True)
    idAsignatura = models.ForeignKey('Asignatura', on_delete=models.CASCADE)
    idCurso = models.ForeignKey('Cursos', on_delete=models.CASCADE)
    idDia = models.ForeignKey('Dias', on_delete=models.CASCADE)
    idAula = models.ForeignKey('Aulas', on_delete=models.CASCADE)
    idProfesor = models.ForeignKey('Profesor', on_delete=models.CASCADE)
    idFranja = models.ForeignKey('FranjaHoraria', on_delete=models.CASCADE, default=1)
    idAusencia = models.ForeignKey('Ausencia', on_delete=models.CASCADE, null=True, blank=True, related_name='horarios')  # <- aquí
    esGuardia = models.BooleanField(default=False)
    fecha = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.idHorario}"



class Ausencia(models.Model):
    idAusencia = models.AutoField(primary_key=True)
    profesor = models.ForeignKey('Profesor', on_delete=models.CASCADE)
    fecha = models.DateField()
    comentario = models.TextField(blank=True)
    horario = models.ForeignKey('Horario', on_delete=models.SET_NULL, null=True, blank=True)
    justificada = models.BooleanField(default=False)