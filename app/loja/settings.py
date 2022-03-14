"""
Django settings for loja project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

# importação para redefinição das mensagens do django
from django.contrib.messages import constants


# FIXME: manter somente em ambiente de desenvolvimento
# importação para o debug-toolbar
import socket


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4h#*k*$whv5+0j24kk1_0rdf*=*fswzyzu+jy9x@prh!&0c^xl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# host incluído para permitir chamada a partir do contêiner
ALLOWED_HOSTS = ['0.0.0.0']


# Application definition

INSTALLED_APPS = [
    'produto',  # declarando o app produto
    'pedido',  # declarando o app pedido
    'perfil',  # declarando o app perfil
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',

    # FIXME: manter somente em ambiente de desenvolvimento
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # FIXME: manter somente em ambiente de desenvolvimento
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'loja.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # definindo a pasta de templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'loja.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'pt-BR'  # configurando as informações de idioma

TIME_ZONE = 'America/Recife'  # configurando as informações de data/hora

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# definindo as pastas de arquivos estáticos
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'templates/static',
]

# definindo as pastas de arquivos de mídia
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# redefinindo as mensagens default do django por classes bootstrap
MESSAGE_TAGS = {
    constants.ERROR: 'alert-danger',
    constants.WARNING: 'alert-warning',
    constants.DEBUG: 'alert-info',
    constants.SUCCESS: 'alert-success',
    constants.INFO: 'alert-info',
}

# redefinindo o template a ser utilizado pelo crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# definindo as regras da sessão
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # duração da sessão
# regra para salvar automaticamente a sessão a cada requisição
SESSION_SAVE_EVERY_REQUEST = False
# SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer' # alteração do serializador default para permitir salvar objetos na sessão


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# FIXME: manter somente em ambiente de desenvolvimento
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + '1' for ip in ips] + ['127.0.0.1', '10.0.2.2']
