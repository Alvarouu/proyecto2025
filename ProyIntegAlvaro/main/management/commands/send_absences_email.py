# main/management/commands/send_absences_email.py

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils.timezone import localtime, now
from main.models import Profesor, Ausencia
from django.conf import settings

class Command(BaseCommand):
    help = 'Envía a los administradores las ausencias programadas para hoy'

    def handle(self, *args, **kwargs):
        today = localtime(now()).date()
        ausencias_hoy = Ausencia.objects.filter(fecha__date=today)

        if not ausencias_hoy.exists():
            self.stdout.write("No hay ausencias programadas hoy.")
            return

        mensaje = "\n".join(
            f"{a.profesor.nombre} {a.profesor.apellido1} - {a.fecha.strftime('%H:%M')}"
            for a in ausencias_hoy
        )

        administradores = Profesor.objects.filter(es_admin=True)
        destinatarios = [admin.correo for admin in administradores if admin.correo]

        if destinatarios:
            send_mail(
                subject="📢 Ausencias programadas para hoy",
                message=mensaje,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=destinatarios,
                fail_silently=False,
            )
            self.stdout.write("Correo enviado a los administradores.")
        else:
            self.stdout.write("No hay administradores con correo válido.")
