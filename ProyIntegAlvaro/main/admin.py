from django.contrib import admin

# Register your models here.
from django.contrib import admin
from main.models import *

admin.site.register(Profesor)
admin.site.register(Asignatura)
admin.site.register(Cursos)
admin.site.register(Aulas)
admin.site.register(Dias)
admin.site.register(FranjaHoraria)
admin.site.register(Horario)
admin.site.register(Ausencia)


