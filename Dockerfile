FROM python:3.10-slim

# Configurar el directorio de trabajo
WORKDIR /app

# Copiar los archivos de la aplicación
COPY . /app

# Instalar las dependencias necesarias del sistema

RUN apt-get update && apt-get install -y \
build-essential \
&& apt-get clean

# Actualizar pip e instalar dependencias de Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Exponer el puerto que usa Django
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
