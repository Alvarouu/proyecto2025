import os
import django
from datetime import date
from django.core.mail import send_mail
from django.conf import settings
from main.models import Ausencia, Profesor

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()


def enviar_ausencias():
    hoy = date.today()
    ausencias_hoy = Ausencia.objects.filter(fecha=hoy)
    if not ausencias_hoy.exists():
        return

    mensaje = "Ausencias programadas para hoy:\n\n"
    for a in ausencias_hoy:
        mensaje += f"- {a.profesor.nombre} {a.profesor.apellido1} ({a.comentario})\n"

    send_mail(
        subject="Ausencias de profesores - Hoy",
        message=mensaje,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[admin[1] for admin in settings.ADMINS],
        fail_silently=False,
    )

if __name__ == "__main__":
    enviar_ausencias()
