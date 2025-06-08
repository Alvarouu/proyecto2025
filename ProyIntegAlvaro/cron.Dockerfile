# cron.Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copiar el crontab
COPY crontab /etc/cron.d/crontab

# Dar permisos
RUN chmod 0644 /etc/cron.d/crontab && \
    crontab /etc/cron.d/crontab

CMD ["cron", "-f"]
