from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from main.models import Profesor, Horario, Ausencia


#Serializadores para profesor, usuario, horario, ausencia, registro y ver ausencia

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = ['idProfesor', 'nombre', 'apellido1', 'apellido2', 'correo', 'password', 'esAdmin', 'idUser']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username']
        extra_kwargs = {'password' : {'write_only': True, 'required': True}}

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user


class HorarioSerializer(serializers.ModelSerializer):
    asignatura = serializers.CharField(source='idAsignatura.nombre')
    curso = serializers.CharField(source='idCurso.nombre')
    aula = serializers.CharField(source='idAula.nombre')
    dia = serializers.CharField(source='idDia.nombre')
    franja = serializers.CharField(source='idFranja.numeroFranja')
    fecha = serializers.DateField(format="%d/%m/%Y")
    hora = serializers.TimeField(source='idFranja.horaInicio', format="%H:%M")


    class Meta:
        model = Horario
        fields = ['asignatura', 'curso', 'aula', 'dia', 'idHorario', 'franja', 'fecha', 'hora']

class RegistrarAusenciaSerializer(serializers.Serializer):
    idHorario = serializers.IntegerField()
    comentario = serializers.CharField(required=False, allow_blank=True)

class AusenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ausencia
        fields = ['idAusencia', 'profesor', 'fecha', 'comentario', 'horario', 'idFranja']

class RegistrarAusenciaSerializer(serializers.Serializer):
    comentario = serializers.CharField(allow_blank=True)
    idHorario = serializers.IntegerField()

class VerAusenciaSerializer(serializers.Serializer):
    idAusencia = serializers.IntegerField()
    fecha = serializers.DateField()
    comentario = serializers.CharField(allow_blank=True)
    profesor_name = serializers.CharField(source='profesor.nombre')
    profesor_ape1 = serializers.CharField(source='profesor.apellido1')
    profesor_ape2 = serializers.CharField(source='profesor.apellido2')
    justificada = serializers.BooleanField()

    class Meta:
        model = Ausencia
        fields = ['idAusencia', 'comentario', 'fecha', 'profesor_name', 'profesor_ape1', 'profesor_ape2', 'justificada']


class VerHorarioSerializer(serializers.ModelSerializer):
    dia = serializers.CharField(source='idDia.nombre', read_only=True)
    franja = serializers.CharField(source='idFranja.descripcion', read_only=True)
    curso = serializers.CharField(source='idCurso.nombre', read_only=True)
    aula = serializers.CharField(source='idAula.nombre', read_only=True)

    class Meta:
        model = Horario
        fields = ['dia', 'franja', 'curso', 'aula']