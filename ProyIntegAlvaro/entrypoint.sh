#!/bin/sh

# Iniciar servicio cron
service cron start

# Ejecutar el comando original (CMD)
exec "$@"