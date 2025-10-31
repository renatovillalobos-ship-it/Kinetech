from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-sw$_&cx=rdqf$+j(dt57hi6@9#v(ghhnwy-8)lmu#uzay5mk$3'



# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #Aplicaciones Propias
    'Applications.Docente',
    'Applications.Estudiante',
    'Applications.Administrador',
    'Applications.Cuestionario',
    'Applications.Caso_Clinico',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Webpage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'Webpage.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [BASE_DIR / "static"]
# 🔹 Agrega esta línea:
STATIC_ROOT = BASE_DIR / "staticfiles"

JAZZMIN_SETTINGS = {
    "site_title": "Kinetech",
    "site_header": "Administradora sistema ",
    "welcome_sign": "Bienvenida al Sistema de Kinetech",
    "site_brand": "Kinetech",
    "site_logo": "img/logo_ucn.jpg",
    "custom_css": "css/admin_custom.css",
    "custom_js": None,
}



MEDIA_ROOT = os.path.join(BASE_DIR, 'media') 
# La URL para acceder a esas fotos (debe ser distinta a STATIC_URL)
MEDIA_URL = '/media/' 

# 2. ARCHIVOS DEL CÓDIGO (STATIC)
STATIC_URL = '/static/'
# Directorio donde Django busca tus archivos estáticos
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'), 
]
