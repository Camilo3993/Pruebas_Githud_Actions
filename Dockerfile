# Establecer la imagen base de Docker a utilizar como Python 3.10
FROM python:3.10

# Exponer el puerto 5000 para permitir conexiones desde fuera del contenedor
EXPOSE 5000

# Establecer el directorio de trabajo dentro del contenedor como /app
WORKDIR /app

# Copiar el archivo requirements.txt del directorio actual del host al directorio /app del contenedor
COPY ./requirements.txt requirements.txt

# Ejecutar el comando pip install para instalar las dependencias listadas en requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copiar todos los archivos del directorio actual del host al directorio /app del contenedor
COPY . .

# Comando que se ejecutará cuando se inicie el contenedor
# Iniciar la aplicación Flask utilizando el comando 'flask run'
# Configurar el host en 0.0.0.0 para que la aplicación esté disponible en todas las interfaces de red del contenedor
CMD ["flask", "run", "--host", "0.0.0.0"]