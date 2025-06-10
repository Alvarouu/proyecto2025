import json
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import permissions, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from main.models import Horario, Ausencia, Cursos, Aulas
from main.serializers import UserSerializer, ProfesorSerializer, HorarioSerializer, AusenciaSerializer, \
    RegistrarAusenciaSerializer, VerAusenciaSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from main.models import Profesor
from django.http import JsonResponse
from datetime import date, timedelta
from django.core.mail import EmailMessage
from django.http import JsonResponse
from main.models import Ausencia, Horario, Profesor
from datetime import date
from io import BytesIO
from xhtml2pdf import pisa
from django.utils import timezone
import datetime


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ProfesorViewSet(request):
    queryset = Profesor.objects.all()
    serializer = ProfesorSerializer(queryset, many=True)

    return Response(serializer.data)

class Generico(GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return User.objects.all()

    @action(methods=['get'], detail=False)
    def me(self, request):
        serializer = self.get_serializer_class()
        data = serializer(request.user).data
        return Response(data, status=status.HTTP_200_OK)

#Metodo que da de alta un profesor en la BBDD
class Registro(GenericViewSet):
    serializer_class = ProfesorSerializer

    def get_queryset(self):
        return Profesor.objects.all()

    def me(self, request):
        serializer_class = self.get_serializer_class()
        data = serializer_class(request.user).data
        return Response(data, status=status.HTTP_200_OK)

    # Metodo que crea un profesor con los campos que le pasa el front y lo serializa
    @action(methods=['post'], detail=False, url_path='register', permission_classes=[IsAuthenticated])
    def register(self, request):
        usuario = User.objects.create_user(username=request.data['correo'],email=request.data['correo'], password=request.data['password'])
        request.data['idUser']= usuario.pk

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Usuario creado correctamente'}, status=201)
        else:
            return Response(serializer.errors, status=400)

    #Metodo para devolver todos los profesores
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

#Metodo de login que comprueba usuario y contraseña, si estan dados de alta genera el token y los devuelve al front
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    correo = request.data.get('correo')
    password = request.data.get('password')
    user = request.user


    if not correo or not password:
        return Response({'error': 'Correo y contraseña requeridos'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username = correo, password = password)
    profesor = Profesor.objects.get(idUser=user)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token':token.key, 'user':user.pk, 'admin':profesor.esAdmin})
    else:
        return Response({'message': 'Usuario no existe'}, status=status.HTTP_401_UNAUTHORIZED)

#Metodo que permite el login con google comparando el token de usuario y el de google
@api_view(['POST'])
@permission_classes([AllowAny])
def google_login_view(request):
    token = request.data.get('token')
    if not token:
        return Response({'error': 'Token requerido'}, status=status.HTTP_400_BAD_REQUEST)
    idinfo = id_token.verify_oauth2_token(token, requests.Request(), '92500515360-q854c10je9ak7o0e9tsl02d6531crjrg.apps.googleusercontent.com')
    email = idinfo['email']
    print(idinfo['email'])
    user = User.objects.get(username=email)
    print(user)
    if user:

        profesor = Profesor.objects.get(idUser=user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token':token.key, 'user':user.pk, 'admin':profesor.esAdmin})
    else:
        return Response({'message': 'Usuario no existe'}, status=status.HTTP_401_UNAUTHORIZED)

#Metodo de logout que comprueba el token del usuario
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout_view(request, user_id):
    token = Token.objects.get(user_id=user_id)
    token.delete()
    return Response({'message': 'Logged out'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def horario_profesor(request):
    user = request.user
    profesor = user.profesor_set.first()
    if not profesor:
        return Response({"detail": "No se encontró el profesor asociado al usuario."}, status=404)

    horarios = Horario.objects.filter(idProfesor=profesor)
    for x in horarios:
        print(type(x.fecha))
    serializer = HorarioSerializer(horarios, many=True)
    return Response(serializer.data)

#Metodo que muestra el horario del profesor logeado con la ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def horarios_profesor_logueado(request):
    profesor = request.user.profesor

    horarios = Horario.objects.filter(idProfesor=profesor).select_related(
        'idAsignatura', 'idCurso', 'idAula', 'idDia', 'idFranja'
    ).order_by('fecha', 'idFranja__numeroFranja')

    for x in horarios:
        print(type(x.fecha))

    resultado = [
        {
            'asignatura': h.idAsignatura.nombre,
            'curso': h.idCurso.nombre,
            'aula': h.idAula.nombre,
            'dia': h.idDia.nombre,
            'franja': h.idFranja.numeroFranja,
            'fecha': h.fecha.strftime('%d/%m/%Y'),
        }
        for h in horarios

    ]

    return JsonResponse(resultado, safe=False)

#Metodo que muestra los datos relevantes del perfil del profesor
@api_view(['GET'])
def perfil_usuario(request):
    user = request.user
    try:
        profesor = Profesor.objects.get(idUser=user)
        return Response({
            'nombre': profesor.nombre,
            'apellido1': profesor.apellido1,
            'apellido2': profesor.apellido2,
            'correo': profesor.correo,
            'esAdmin': profesor.esAdmin,
            'username': user.username
        })
    except Profesor.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=404)

#Metodo que permite cambiar la contraseña de la cuenta profesor
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cambiar_contrasenia(request):
    nueva_contrasenia = request.data.get('nueva_contrasenia')

    if not nueva_contrasenia:
        return Response({'error': 'Se requiere una nueva contraseña.'}, status=status.HTTP_400_BAD_REQUEST)

    user = request.user
    user.set_password(nueva_contrasenia)
    user.save()

    # Actualizar también la contraseña en el modelo Profesor
    try:
        profesor = Profesor.objects.get(idUser=user)
        profesor.password = user.password  # Guardamos el hash
        profesor.save()
    except Profesor.DoesNotExist:
        return Response({'error': 'No se encontró el profesor asociado.'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'mensaje': 'Contraseña actualizada correctamente.'}, status=status.HTTP_200_OK)

#Metodo que filtra los horarios por la semana actual
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def clases_semana_actual(request):
    user = request.user
    profesor = Profesor.objects.get(idUser=user)
    print(profesor)
    hoy = date.today()
    print(hoy)
    # Calcular lunes y domingo de la semana actual
    lunes = hoy - timedelta(days=hoy.weekday())  # weekday() lunes=0
    domingo = lunes + timedelta(days=6)
    print(type(domingo))
    print(type(lunes))
    horarios = Horario.objects.filter(
        idProfesor=profesor,
        fecha__gte=lunes,
        fecha__lte=domingo
    ).select_related('idAsignatura', 'idCurso', 'idAula', 'idDia', 'idFranja'
    ).order_by('fecha', 'idFranja__numeroFranja')
    print(horarios)
    resultado = [
        {
            'asignatura': h.idAsignatura.nombre,
            'curso': h.idCurso.nombre,
            'aula': h.idAula.nombre,
            'dia': h.idDia.nombre,
            'franja': h.idFranja.numeroFranja,
            'fecha': h.fecha.strftime('%d/%m/%Y'),
            'hora': h.idFranja.horaInicio.strftime('%H:%M')
        }
        for h in horarios
    ]

    return JsonResponse(resultado, safe=False)


# Metodo para registrar una ausencia que puede llevar un comentario
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def registrar_ausencia(request):
    serializer = RegistrarAusenciaSerializer(data=request.data)

    if serializer.is_valid():
        idhorario = serializer.validated_data['idHorario']
        comentario = serializer.validated_data.get('comentario', '')

        try:
            profesor = Profesor.objects.get(idUser=request.user)
        except Profesor.DoesNotExist:
            return Response({'error': 'No se encontró el profesor vinculado al usuario'},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            horario = Horario.objects.get(idHorario=idhorario)
        except Horario.DoesNotExist:
            return Response({'error': 'Horario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        # Usamos la fecha del horario o fallback a hoy
        fecha_ausencia = horario.fecha if horario.fecha else timezone.now().date()

        # Crear la ausencia y asignar idFranja desde el horario
        ausencia = Ausencia.objects.create(
            profesor=profesor,
            horario=horario,
            fecha=fecha_ausencia,
            comentario=comentario,
            idFranja=horario.idFranja  # ← Aquí asignamos idFranja desde el horario seleccionado
        )

        return Response(AusenciaSerializer(ausencia).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HorariosPorProfesorAPIView(APIView):
    def get(self, request, usuario_id):
        horarios = Horario.objects.filter(idProfesor__idUser_id=usuario_id)
        serializer = HorarioSerializer(horarios, many=True)
        return Response(serializer.data)

#Metodo que muestra las ausencias que hay disponibles
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def consultar_ausencia(request):
    ausencias = Ausencia.objects.all()
    serializer = VerAusenciaSerializer(ausencias, many=True)

    return Response(serializer.data)

#Metodo que justifica o no justifica una ausencia
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def justificar(request):
    id_ausencia = request.data.get('id')
    justificar = request.data.get('justificar')
    if id_ausencia is None or justificar is None:
        return Response({'error': 'Faltan datos: id y justificar'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        ausencia = Ausencia.objects.get(pk=id_ausencia)
    except Ausencia.DoesNotExist:
        return Response({'error': 'Ausencia no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    ausencia.justificada = justificar
    ausencia.save()

    return Response({'mensaje': f'Ausencia {"justificada" if justificar else "no justificada"} correctamente'},
                    status=status.HTTP_200_OK)

#Metodo que filtra los horarios por el aula
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_aulas(request):
    usuario_id = request.user.id  # ID del usuario logueado

    # Filtramos las aulas relacionadas con el profesor logueado
    aulas_ids = Horario.objects.filter(
        idProfesor__idUser_id=usuario_id
    ).values_list('idAula', flat=True).distinct()

    if not aulas_ids:
        return Response([], status=200)

    aulas = Aulas.objects.filter(idAula__in=aulas_ids).order_by('nombre')
    data = [{'id': a.idAula, 'nombre': a.nombre} for a in aulas]
    return Response(data)

#Metodo que filtra los horarios por curso
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_cursos(request):
    usuario_id = request.user.id  # ID del usuario logueado

    # Filtramos los cursos relacionados con el profesor logueado
    cursos_ids = Horario.objects.filter(
        idProfesor__idUser_id=usuario_id
    ).values_list('idCurso', flat=True).distinct()

    if not cursos_ids:
        return Response([], status=200)

    cursos = Cursos.objects.filter(idCurso__in=cursos_ids).order_by('nombre')
    data = [{'id': c.idCurso, 'nombre': c.nombre} for c in cursos]
    return Response(data)

#Metodo que filtra los horarios por aula
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def horarios_por_aula(request, aula_id):
    usuario_id = request.user.id

    # Filtramos los horarios del profesor logueado en esa aula
    horarios = Horario.objects.filter(
        idProfesor__idUser_id=usuario_id,
        idAula_id=aula_id
    ).select_related('idAsignatura', 'idCurso', 'idAula', 'idDia', 'idFranja')

    serializer = HorarioSerializer(horarios, many=True)
    return Response(serializer.data)

#Metodo que filtra los horarios por curso
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def horarios_por_curso(request, curso_id):
    usuario_id = request.user.id

    # Filtramos los horarios del profesor logueado en ese curso
    horarios = Horario.objects.filter(
        idProfesor__idUser_id=usuario_id,
        idCurso_id=curso_id
    ).select_related('idAsignatura', 'idCurso', 'idAula', 'idDia', 'idFranja')

    serializer = HorarioSerializer(horarios, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enviar_informe_ausencias(request):
    user = request.user

    try:
        profesor_destino = Profesor.objects.get(idUser=user)
    except Profesor.DoesNotExist:
        return JsonResponse({'error': 'No se encontró al profesor asociado al usuario.'}, status=404)

    hoy = timezone.now().date()

    # Buscar ausencias de hoy
    ausencias_del_dia = Ausencia.objects.filter(fecha=hoy)

    if not ausencias_del_dia.exists():
        return JsonResponse({'mensaje': 'No hay ausencias hoy.'}, status=204)

    datos_ausencias = []
    datos_guardias = []

    for ausencia in ausencias_del_dia:
        id_franja = ausencia.idFranja

        if not id_franja:
            continue  # Saltamos si no tiene franja horaria

        horarios_profesor = Horario.objects.filter(
            idProfesor=ausencia.profesor,
            idFranja=id_franja,
            fecha=hoy
        )

        for horario in horarios_profesor:
            guardias = Horario.objects.filter(
                idFranja=id_franja,
                fecha=hoy,
                esGuardia=True
            ).exclude(idProfesor=ausencia.profesor)

            datos_ausencias.append({
                'profesor': f"{ausencia.profesor.nombre} {ausencia.profesor.apellido1}",
                'hora': id_franja.horaInicio.strftime('%H:%M') if id_franja.horaInicio else 'Sin hora',
                'curso': horario.idCurso.nombre if horario.idCurso and horario.idCurso.nombre.strip() else 'Sin curso',
                'aula': horario.idAula.nombre if horario.idAula and horario.idAula.nombre.strip() else 'Sin aula'
            })

            if guardias.exists():
                datos_guardias.append({
                    'profesor': f"{ausencia.profesor.nombre} {ausencia.profesor.apellido1}",
                    'guardias': ', '.join(f"{g.idProfesor.nombre} {g.idProfesor.apellido1}" for g in guardias),
                })
            else:
                datos_guardias.append({
                    'profesor': f"{ausencia.profesor.nombre} {ausencia.profesor.apellido1}",
                    'guardias': 'No hay guardias asignadas'
                })

    if not datos_ausencias:
        return JsonResponse({'mensaje': 'No hay datos de ausencias para generar el informe.'}, status=204)

    # Generar HTML
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            h2 {{ text-align: center; color: #333; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 10px; border: 1px solid #ccc; text-align: left; }}
            th {{ background-color: #f2f2f2; color: #444; }}
        </style>
    </head>
    <body>
        <h2>Informe de Ausencias - {hoy.strftime('%d/%m/%Y')}</h2>
        <p>Estimado/a {profesor_destino.nombre},</p>
        <p>Se adjunta el informe de ausencias del día:</p>

        <!-- Tabla 1: Datos de ausencias -->
        <h3>Ausencias del Día</h3>
        <table>
            <thead>
                <tr>
                    <th>Profesor Ausente</th>
                    <th>Hora</th>
                    <th>Curso</th>
                    <th>Aula</th>
                </tr>
            </thead>
            <tbody>
    """

    for item in datos_ausencias:
        html += f"""
                <tr>
                    <td>{item['profesor']}</td>
                    <td>{item['hora']}</td>
                    <td>{item['curso']}</td>
                    <td>{item['aula']}</td>
                </tr>
        """

    html += """
            </tbody>
        </table>

        <!-- Tabla 2: Guardias Asignadas -->
        <h3>Guardias Asignadas</h3>
        <table>
            <thead>
                <tr>
                    <th>Profesor Ausente</th>
                    <th>Guardias</th>
                </tr>
            </thead>
            <tbody>
    """

    for item in datos_guardias:
        html += f"""
                <tr>
                    <td>{item['profesor']}</td>
                    <td>{item['guardias']}</td>
                </tr>
        """

    html += """
            </tbody>
        </table>
    </body>
    </html>
    """

    # Generar PDF
    buffer = BytesIO()
    pisa.CreatePDF(src=html, dest=buffer)
    pdf = buffer.getvalue()
    buffer.close()

    if not pdf:
        return JsonResponse({'error': 'El PDF está vacío.'}, status=500)

    # Enviar correo
    email = EmailMessage(
        subject=f"Informe de Ausencias - {hoy.strftime('%d/%m/%Y')}",
        body="Adjunto se encuentra el informe de ausencias del día.",
        to=[profesor_destino.correo]
    )
    email.attach(f'InformeAusencias_{hoy}.pdf', pdf, 'application/pdf')

    try:
        email.send()
        print("Correo enviado a:", profesor_destino.correo)
        return JsonResponse({'mensaje': '📧 Correo enviado correctamente'})
    except Exception as e:
        return JsonResponse({'error': f'Error al enviar el correo: {str(e)}'}, status=500)