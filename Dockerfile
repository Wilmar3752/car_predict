# Usar una imagen base de Python
FROM python:3.10
ARG CODE=/app
# Establecer el directorio de trabajo en /app
WORKDIR $CODE

# Copiar los archivos de requisitos y el archivo Dockerfile en el contenedor
COPY . $CODE
#COPY .env ./

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Establecer PYTHONPATH al directorio raíz
#ENV PYTHONPATH "${PYTHONPATH}:/app"

# Exponer el puerto 8000 para que otros contenedores puedan acceder a tu API
EXPOSE 7860

# Comando para iniciar la aplicación 7860 para huggingface 8080 para local
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]
