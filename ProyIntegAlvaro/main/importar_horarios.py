import os
from datetime import date, timedelta, datetime, time
from django.contrib.auth.models import User
from main.models import Profesor, Asignatura, Cursos, Aulas, Dias, FranjaHoraria, Horario

# Mapeo de nombre de día a weekday() (0=Lunes, ..., 6=Domingo)
weekday_map = {
    'Lunes': 0,
    'Martes': 1,
    'Miércoles': 2,
    'Jueves': 3,
    'Viernes': 4,
}

def fecha_del_dia_de_esta_semana(nombre_dia):
    weekday_deseado = weekday_map.get(nombre_dia)
    if weekday_deseado is None:
        raise ValueError(f"Día no válido: {nombre_dia}")

    hoy = date.today()
    lunes_esta_semana = hoy - timedelta(days=hoy.weekday())  # lunes de esta semana
    fecha_deseada = lunes_esta_semana + timedelta(days=weekday_deseado)
    return fecha_deseada

# Crear franjas horarias con hora de inicio
franjas_definidas = [
    ("1ª clase", False), ("2ª clase", False), ("3ª clase", False),
    ("Recreo (mañana)", True),
    ("4ª clase", False), ("5ª clase", False), ("6ª clase", False),
    ("7ª clase", False), ("8ª clase", False), ("9ª clase", False),
    ("Recreo (tarde)", True),
    ("10ª clase", False), ("11ª clase", False), ("12ª clase", False),
]

hora_inicio_base = time(8, 15)
minutos_transcurridos = 0

for i, (descripcion, es_recreo) in enumerate(franjas_definidas, start=1):
    hora_actual = (datetime.combine(date.today(), hora_inicio_base) + timedelta(minutes=minutos_transcurridos)).time()
    duracion = 30 if es_recreo else 60
    minutos_transcurridos += duracion

    FranjaHoraria.objects.update_or_create(
        numeroFranja=i,
        defaults={
            'descripcion': descripcion,
            'esRecreo': es_recreo,
            'horaInicio': hora_actual,
        }
    )

# Procesar archivo
file_path = 'main/Datos_horarios.txt'
dias_map = {'L': 'Lunes', 'M': 'Martes', 'X': 'Miércoles', 'J': 'Jueves', 'V': 'Viernes'}

with open(file_path, 'r', encoding='utf-8') as f:
    for linea in f:
        partes = linea.strip().split('\t')
        if len(partes) < 6:
            continue

        asignatura_txt, curso_txt, aula_txt, profesor_txt, dia_abrev, franja_str = partes

        asignatura, _ = Asignatura.objects.get_or_create(nombre=asignatura_txt)
        curso, _ = Cursos.objects.get_or_create(nombre=curso_txt)
        aula, _ = Aulas.objects.get_or_create(nombre=aula_txt if aula_txt else "Sin aula")
        dia_nombre = dias_map.get(dia_abrev, dia_abrev)
        dia, _ = Dias.objects.get_or_create(nombre=dia_nombre)
        franja, _ = FranjaHoraria.objects.get_or_create(
            numeroFranja=int(franja_str),
            defaults={'descripcion': f'Franja {franja_str}'}
        )

        try:
            apellidos, nombre = profesor_txt.split(',')
            apellido_parts = apellidos.strip().split(' ')
            apellido1 = apellido_parts[0]
            apellido2 = apellido_parts[1] if len(apellido_parts) > 1 else ''
            nombre = nombre.strip()
        except Exception as e:
            print(f"❌ Error procesando nombre del profesor: {profesor_txt} - {e}")
            continue

        correo = f"{nombre.lower()}{apellido1.lower()}@iespoligonosur.org".replace(' ', '')
        user = User.objects.filter(username=correo).first()
        if not user:
            user = User(username=correo, first_name=nombre, last_name=f"{apellido1} {apellido2}".strip(), email=correo)
            user.set_password('1234')
            user.save()

        profesor = Profesor.objects.filter(nombre=nombre, apellido1=apellido1, apellido2=apellido2).first()
        if not profesor:
            profesor = Profesor.objects.create(
                nombre=nombre, apellido1=apellido1, apellido2=apellido2,
                correo=correo, password=user.password, esAdmin=False, idUser=user
            )

        fecha_ordenada = fecha_del_dia_de_esta_semana(dia_nombre)

        horario_existente = Horario.objects.filter(
            idAsignatura=asignatura,
            idCurso=curso,
            idAula=aula,
            idProfesor=profesor,
            idDia=dia,
            idFranja=franja,
            fecha=fecha_ordenada
        ).exists()

        if not horario_existente:
            Horario.objects.create(
                idAsignatura=asignatura,
                idCurso=curso,
                idAula=aula,
                idProfesor=profesor,
                idDia=dia,
                idFranja=franja,
                esGuardia=False,
                fecha=fecha_ordenada
            )
            print(f"✔ Añadido: {asignatura_txt}, {curso_txt}, {dia_nombre}, Franja {franja_str}, Fecha: {fecha_ordenada}")
        else:
            print(f"⏩ Duplicado: {asignatura_txt}, {curso_txt}, {dia_nombre}, Franja {franja_str}, Fecha: {fecha_ordenada}")

print("✅ Importación finalizada.")
