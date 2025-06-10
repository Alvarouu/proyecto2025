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
        return f"{self.nombre} {self.apellido1}"


class Asignatura(models.Model):
    idAsignatura = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Cursos(models.Model):
    idCurso = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Aulas(models.Model):
    idAula = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Dias(models.Model):
    idDia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class FranjaHoraria(models.Model):
    idFranjaHoraria = models.AutoField(primary_key=True)
    numeroFranja = models.IntegerField()
    descripcion = models.CharField(max_length=50)
    esRecreo = models.BooleanField(default=False)
    horaInicio = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.descripcion} ({self.numeroFranja}ª)"

class Horario(models.Model):
    idHorario = models.AutoField(primary_key=True)
    idAsignatura = models.ForeignKey('Asignatura', on_delete=models.CASCADE)
    idCurso = models.ForeignKey('Cursos', on_delete=models.CASCADE)
    idDia = models.ForeignKey('Dias', on_delete=models.CASCADE)
    idAula = models.ForeignKey('Aulas', on_delete=models.CASCADE)
    idProfesor = models.ForeignKey('Profesor', on_delete=models.CASCADE)
    idFranja = models.ForeignKey('FranjaHoraria', on_delete=models.CASCADE, default=1)
    idAusencia = models.ForeignKey('Ausencia', on_delete=models.CASCADE, null=True, blank=True, related_name='horarios')
    esGuardia = models.BooleanField(default=False)
    fecha = models.DateField(null=True, blank=True)

    def __str__(self):
        profesor_nombre = f"{self.idProfesor.nombre} {self.idProfesor.apellido1}" if self.idProfesor else "Sin profesor"
        curso_nombre = self.idCurso.nombre if self.idCurso else "Sin curso"
        dia_nombre = self.idDia.nombre if self.idDia else "Sin día"
        franja_descripcion = self.idFranja.descripcion if self.idFranja else "Sin franja"

        return f"{profesor_nombre} - {curso_nombre}, {dia_nombre}, {franja_descripcion}"



class Ausencia(models.Model):
    idAusencia = models.AutoField(primary_key=True)
    profesor = models.ForeignKey('Profesor', on_delete=models.CASCADE)
    fecha = models.DateField()
    comentario = models.TextField(blank=True)
    horario = models.ForeignKey('Horario', on_delete=models.SET_NULL, null=True, blank=True)
    idFranja = models.ForeignKey('FranjaHoraria', on_delete=models.CASCADE, null=True)
    justificada = models.BooleanField(default=False)

    def __str__(self):
        profesor_nombre = f"{self.profesor.nombre} {self.profesor.apellido1}" if self.profesor else "Sin profesor"
        franja = self.idFranja.descripcion if self.idFranja else "Sin franja"
        return f"Ausencia de {profesor_nombre} - {self.fecha} | Franja: {franja}"