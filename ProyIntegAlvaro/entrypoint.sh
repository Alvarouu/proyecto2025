#!/bin/sh

# Iniciar servicio cron
service cron start

# Recoger archivos estáticos
python manage.py collectstatic --noinput

# Ejecutar el comando original (CMD)
exec "$@"