# Imagen base oficial de Python
FROM python:3.13-slim

# Evitar la creación de archivos .pyc y habilitar salida directa en consola
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para PostgreSQL y librerías C
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto al contenedor
COPY . /app/

# Exponer el puerto estándar de Django
EXPOSE 8000

# Comando para desarrollo con hot-reloading
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
