from django.core.management.base import BaseCommand
from django.utils.timezone import localdate
from main.models import Ausencia, Horario
from django.core.mail import EmailMessage
from io import BytesIO
from reportlab.pdfgen import canvas

#Comando que envia las ausencias del dia de hoy junto con los profesores que esten de guardia en el dia
class Command(BaseCommand):
    help = 'Envía por correo las ausencias y guardias del día en formato PDF'

    def handle(self, *args, **kwargs):
        hoy = localdate()

        ausencias = Ausencia.objects.filter(fecha=hoy)
        guardias = Horario.objects.filter(fecha=hoy, esGuardia=True)

        if not ausencias.exists() and not guardias.exists():
            self.stdout.write("No hay ausencias ni guardias hoy.")
            return

        # Crear PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.setTitle(f"Avisos {hoy}")

        y = 800
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, y, f"Avisos del día {hoy}")
        y -= 40

        # Ausencias
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y, "Profesores con ausencia:")
        y -= 20

        if ausencias.exists():
            p.setFont("Helvetica", 11)
            for ausencia in ausencias:
                prof = ausencia.profesor
                texto = f"- {prof.nombre} {prof.apellido1} {prof.apellido2} ({prof.correo})"
                p.drawString(110, y, texto)
                y -= 15
        else:
            p.drawString(110, y, "Ninguno.")
            y -= 15

        y -= 20

        # Guardias
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y, "Profesores con guardia:")
        y -= 20

        if guardias.exists():
            p.setFont("Helvetica", 11)
            for guardia in guardias:
                prof = guardia.idProfesor
                franja = guardia.idFranja.descripcion if guardia.idFranja else "Sin franja"
                aula = guardia.idAula.nombre if guardia.idAula else "Sin aula"
                texto = f"- {prof.nombre} {prof.apellido1} {prof.apellido2} ({prof.correo}) | {franja} | Aula: {aula}"
                p.drawString(110, y, texto)
                y -= 15
        else:
            p.drawString(110, y, "Ninguno.")
            y -= 15

        p.showPage()
        p.save()

        buffer.seek(0)
        pdf_file = buffer.getvalue()

        # Enviar correo
        email = EmailMessage(
            subject=f"Avisos de ausencias y guardias ({hoy})",
            body="Se adjunta el informe PDF con los avisos del día.",
            from_email="alvarouu@gmail.com",
            to=["alvarouu@gmail.com"],
        )
        email.attach(f"avisos_{hoy}.pdf", pdf_file, "application/pdf")
        email.send()

        self.stdout.write(f"Correo enviado. Ausencias: {ausencias.count()} | Guardias: {guardias.count()}")
