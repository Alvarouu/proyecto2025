from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from django.contrib import admin
from main import views
from main.views import Generico, Registro, login_view, logout_view, ProfesorViewSet, horario_profesor, \
    horarios_profesor_logueado, perfil_usuario, cambiar_contrasenia, clases_semana_actual, registrar_ausencia, \
    HorariosPorProfesorAPIView, consultar_ausencia, justificar, listar_cursos, \
    listar_aulas, horarios_por_curso, horarios_por_aula, google_login_view, enviar_informe_ausencias

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

router = DefaultRouter()
router.register(r'registro', Registro, basename='registro')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('users/me', Generico.as_view({'get': 'me'}), name="user_view_set"),
    path('login/', login_view, name='login'),
    path('logout/<int:user_id>', logout_view, name='logout'),
    path('horario/', horario_profesor, name='horario-profesor'),
    path('api/horarios/', horarios_profesor_logueado),
    path('perfil/', perfil_usuario),
    path('cambiar-contrasenia/', cambiar_contrasenia, name='cambiar_contrasenia'),
    path('horario/semana/', clases_semana_actual, name='clases_semana_actual'),
    path('registrar-ausencia/', registrar_ausencia, name='registrar-ausencia'),
    path('horarios-profesor/<int:usuario_id>/', HorariosPorProfesorAPIView.as_view(), name='horarios-profesor'),
    path('consultar-ausencia/', consultar_ausencia, name='consultar-ausencia'),
    path('justificar/', justificar, name='justificar'),
    path('profesores/', ProfesorViewSet, name='ProfesorViewSet'),
    path('horario/cursos/', listar_cursos, name='listar_cursos'),
    path('horario/aulas/', listar_aulas, name='listar_aulas'),
    path('horario/aula/<int:aula_id>/', horarios_por_aula, name='horarios_por_aula'),
    path('horario/curso/<int:curso_id>/', horarios_por_curso, name='horarios_por_curso'),
    path('loginG/', google_login_view, name='google_login_view'),
    path('informe-ausencia/', enviar_informe_ausencias, name='informe-ausencia'),

]

