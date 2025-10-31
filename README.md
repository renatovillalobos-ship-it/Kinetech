# Kinetech
Repositorio github para el desarrollo de una plataforma web.
Nombre del proyecto: Proyecto educativo de kinesiología.

Descripción:
El sistema tiene como objetivo apoyar el proceso de aprendizaje de los estudiantes de kinesiología mediante la implementación de un sitio web que presente recursos audiovisuales y formularios que fortalezcan los conocimientos sobre la práctica de anamnesis (entrevista clínica inicial del paciente).

Integrantes del equipo:
Pía González
Matías González
Alexandra Herrera
Javiera Morales
Renato Padilla
Camila Ramos -> Product owner
Renato Villalobos -> Scrum master

Instrucciones de instalación y ejecución:
1. Estar en la carpeta del proyecto: debes ubicarte  donde se encuentra el archivo README.md, ingresar a la carpeta 'aplicacion' y copiar la ruta que se encuentra en la barra superior.
2. Utilizar Símbolo del Sistema (CMD): dentro del CMD debes crear el entorno virtual. Utilizando el comando cd para navegar entre carpetas debes ingresar a la ruta copiada anteriormente (carpeta aplicacion) y utilizar el siguiente comando:
         - Python -m venv Nombre del Entorno
Posteriormente debes ingresar a la carpeta del entorno que acabas de crear y entrar a la carpeta Scripts:
Deberías visualizar esto:  - “Nombre del Entorno” / Scripts
Luego debes utilizar el comando 'activate' para activar el entorno. 

3. Instalación de recursos necesarios para la utilización de la aplicación:
  Para instalar las librerías existen 2 formas (para ambas debes cambiar de carpeta ya sea utilizando el comando cd.. o copiando nuevamente la ruta a donde quieres moverte, en este caso debes ubicarte a la altura del archivo manage.py:
    a) Mediante el archivo requirements.txt que contiene todas las librerías a utilizar junto a la versión que debe instalarse. Esto se realiza mediante el Símbolo del
       Sistema (CMD) ingresando a la carpeta en donde se encuentre el archivo (cd nombre de la carpeta o ruta) y luego instalar con el comando: pip install -r requirements.txt
    b)De forma manual: las instalaciones deben realizarse en Símbolo del Sistema (CMD) en el siguiente orden:
        I. pip install django
        II. pip install psycopg2
        III. pip install pillow
        IV. pip install jazzmin

Información sobre cada Recurso instalado:
        -pip install django: Permite crear y ejecutar el proyecto
        -pip install psycopg2: Permite a Python interactuar con la base de datos de PostgreSql.
        -pip install pillow: Permite poder trabajar con imágenes dentro del proyecto
        -pip install jazzmin: Permite editar colores, y formatos dentro del sitio web.
  
4.Navega a la carpeta settings dentro del proyecto (/Webpage/settings/) y dentro de esa carpeta crea un archivo nuevo llamado local.py con el siguiente contenido:

from .base import *
DEBUG = True

ALLOWED_HOST = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<db_nombre>', #Ingresar  nombre de tu base de datos PostgreSQL
        'USER': '<user_NombreDeUser>', #Tu usuario de PostgreSQL
        'PASSWORD': '<db_password>', #Tu contraseña de PostgreSQL
        'HOST': 'localhost',
        'PORT': '5432' <ingresar puerto en caso de que sea distinto al por defecto)
    }
}


STATIC_URL = 'static/'

#Recordar eliminar los <> dentro de DATABASE para evitar conflictos.

5. Aplicamos migraciones: los comandos estarán listado por orden de utilización, estos de deben de utilizar uno por uno dentro del Símbolo del Sistema (cmd).
        I. python manage.py makemigrations
        II. python manage.py migrate
   
6. Comando para ejecutar Aplicación:
        - python manage.py runserver
Al aplicar este comando dentro del Símbolo del Sistema nos dará el URL para poder abrir proyecto dentro del navegador. Se debe de visualizar de esta manera: http://127.0.0.1:8000


Datos de conexión a la BD:
Motor: PostgreSQL
ENGINE: 'django.db.backends.postgresql_psycopg2'
Nombre BD: <db_nombre>
Usuario: <db_user>
Contraseña: <db_password>
Host: localhost
Puerto: 5432
