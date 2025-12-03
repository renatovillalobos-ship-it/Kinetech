from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-sw$_&cx=rdqf$+j(dt57hi6@9#v(ghhnwy-8)lmu#uzay5mk$3'


DEBUG = True  # Asegúrate que sea True para desarrollo
ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # <- Agregar esto si no está


# ==============================================================================
# CONFIGURACIÓN DE SESIONES PARA "RECORDARME"
# ==============================================================================

# Motor de sesiones (base de datos recomendado)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Tiempo de expiración de la sesión (30 días en segundos)
SESSION_COOKIE_AGE = 2592000

# La sesión NO expira cuando se cierra el navegador (permite "Recordarme")
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Renovar la sesión en cada petición (recomendado para mejor UX)
SESSION_SAVE_EVERY_REQUEST = True

# Configuración de cookies de sesión
SESSION_COOKIE_SECURE = False  # True en producción con HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'




# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # <- AÑADIR ESTO
    
    
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
        'DIRS': [BASE_DIR /'templates'],
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
        ############
    # Top Menu #
    ############


      # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

        # external url that opens in a new window (Permissions can be added)
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},

        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "Caso_Clinico"},
        {"app": "Cuestionario"},
        {"app": "Docente"},
        {"app": "Estudiante"},
    ],
     #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        {"model": "auth.user"}
    ],
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



# ============================================
# CONFIGURACIÓN EMAIL - RESTABLECIMIENTO
# ============================================

# Para desarrollo - Muestra emails en consola
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Configuración personalizada
DEFAULT_FROM_EMAIL = 'soporte@sistema-ucn.cl'
SITE_ID = 1  # Importante para que funcione correctamente

# Hosts permitidos para desarrollo
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# ============================================
# CONFIGURACIÓN DE AUTENTICACIÓN
# ============================================

# Redirección después de login/logout
LOGIN_URL = '/login/'  # O la URL de tu login
LOGIN_REDIRECT_URL = '/'  # Página después de login exitoso
LOGOUT_REDIRECT_URL = '/login/'  # Página después de logout

# Tiempo de expiración del token de restablecimiento (24 horas en segundos)
PASSWORD_RESET_TIMEOUT = 86400