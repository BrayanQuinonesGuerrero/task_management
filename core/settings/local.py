from .base import *


env.read_env('.env.local')

DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = tuple(env.list('ALLOWED_HOSTS'))

SECRET_KEY = env.str('SECRET_KEY')


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Para pruebas locales
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'