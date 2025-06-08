FROM python:3.11-slim

# Instalar cron
RUN apt-get update && \
    apt-get install -y cron && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Copiar script de cron
COPY crontab /etc/cron.d/send_absences

# Dar permisos al cron script
RUN chmod 0644 /etc/cron.d/send_absences

# Registrar el cron job
RUN crontab /etc/cron.d/send_absences

# Crear log file
RUN touch /var/log/cron.log

# Copiar y dar permisos al entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Entrada del contenedor
ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "main.wsgi:application", "--bind", "0.0.0.0:9000"]