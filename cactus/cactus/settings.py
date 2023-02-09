"""
Django settings for cactus project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import environ
from datetime import timedelta

SITE = os.getenv("SITE", "local")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env()
if (os.path.isfile(os.path.join(BASE_DIR, '.env')) or
   os.path.isfile(env.str('ENV_PATH', ''))):
    env.read_env(env.str('ENV_PATH', os.path.join(BASE_DIR, '.env')))
PROD = env.bool('PRODUCTION', False)
if (PROD):
    USE_S3 = env.bool('USE_S3', True)
else:
    USE_S3 = env.bool('USE_S3', False)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = env('DJANGO_SECRET_KEY')
SECRET_KEY = 'nqmxj(1i%0i%5w1we&va-r8l7uyr6dbm$q6^x3#!5#364d1ox8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', True)

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'staging.inguz.site',
                 'test.inguz.site', 'prod.inguz.site',
                 'staging.zygoo.mx', 'test.zygoo.mx',
                 'inguz.site', 'zygoo.mx', '10.195.1.207',
                 '10.5.1.1', 'inguzmx.com', 'staging.inguz.online',
                 'test.inguz.online']

RECAPTCHA_PUBLIC_KEY = '6Lc_Z2ojAAAAAIi_BPRSrrmkle33Yk9pf4JtWEsQ'
RECAPTCHA_PRIVATE_KEY = '6Lc_Z2ojAAAAAKxXKQwxFosKmzM7SHxxuKn2w1zP'
RECAPTCHA_REQUIRED_SCORE = 0.85

# Application definition

INSTALLED_APPS = [
    'rest_framework.authtoken',
    'rest_framework',
    'corsheaders',
    'multi_captcha_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django_countries',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'graphene_django',
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig',
    'reportlab',
    'rangefilter',
    'notifications',
    'django_extensions',
    'axes',
    # Nuestras apps internas
    'CactusDBLogger',
    'banca.apps.BancaConfig',
    'demograficos.apps.DemograficosConfig',
    'administradores.apps.AdministradoresConfig',
    'contabilidad.apps.ContabilidadConfig',
    'dde.apps.DdeConfig',
    'servicios.apps.ServiciosConfig',
    'pld.apps.PldConfig',
    'legal.apps.LegalConfig',
    'spei.apps.SpeiConfig',
    'prueba.apps.PruebaConfig',
    'seguros.apps.SegurosConfig',
    'generador.apps.GeneradorConfig',
    'pagos.apps.PagosConfig',
    'pagos.rapydcollect.apps.RapydcollectConfig',
    'scotiabank.apps.ScotiabankConfig',
    'renapo.apps.RenapoConfig',
    'dapp.apps.DappConfig',
    'crecimiento.apps.CrecimientoConfig',
]

if (PROD):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env.str('POSTGRES_NAME', 'inguz'),
            'USER': env.str('POSTGRES_USER'),
            'PASSWORD': env.str('POSTGRES_PASSWORD'),
            'HOST': env.str('POSTGRES_HOST'),
            'PORT': env.int('POSTGRES_PORT', 5432)
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
        }
    }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'cactus.token_auth.TokenAuthenticationMulti',
    ]
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_auto_logout.middleware.auto_logout',
    'axes.middleware.AxesMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = ['http://localhost:5000',
                         'https://localhost:5000',
                         'http://localhost:9000',
                         'http://127.0.0.1:9000',
                         'http://127.0.0.1:5000',
                         'https://inguz.netlify.app',
                         'https://10.195.1.207:8000',
                         'https://10.195.1.207',
                         'http://10.195.1.207:8000',
                         'http://10.195.1.207',
                         'https://10.5.1.1:8000',
                         'https://10.5.1.1',
                         'http://10.5.1.1',
                         'http://10.5.1.1:8000',
                         'http://inguzmx.com',
                         'https://inguzmx.com', ]


ROOT_URLCONF = 'cactus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_auto_logout.context_processors.auto_logout_client',
            ],
        },
    },
]

WSGI_APPLICATION = 'cactus.wsgi.application'

GRAPHENE = {
    'SCHEMA': 'cactus.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

MULTI_CAPTCHA_ADMIN = {
    'engine': 'recaptcha2',
}

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
    'cactus.customAuthBackend.EmailBackend',
]


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
GRAPHQL_JWT = {
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_EXPIRATION_DELTA': timedelta(hours=4),
    "JWT_REFRESH_EXPIRATION_DELTA": timedelta(hours=4),
    'JWT_ALLOW_ARGUMENT': True,
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.\
UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.\
MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.\
CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.\
NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'es-MX'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s \
                %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'db_log': {
            'level': 'DEBUG',
            'class': 'CactusDBLogger.db_log_handler.DatabaseLogHandler'
        },
    },
    'loggers': {
        'db': {
            'handlers': ['db_log'],
            'level': 'DEBUG'
        }
    }
}

# S3

if (USE_S3):
    AWS_ACCESS_KEY_ID = env.str('AWS_KEY_ID', "")
    AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ID', "")
    AWS_STORAGE_BUCKET_NAME = 'phototest420'
    AWS_S3_REGION_NAME = 'us-east-1'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_DEFAULT_ACL = None
    # s3 static settings
    AWS_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'cactus.storage_backends.StaticStorage'
    # s3 private media settings
    PRIVATE_MEDIA_LOCATION = 'docs'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PRIVATE_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'cactus.storage_backends.PrivateMediaStorage'
else:
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.2/howto/static-files/
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

RENAPO_USER = env.str("RENAPO_USER", "")
RENAPO_PASSWORD = env.str("RENAPO_PASSWORD", "")

# STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
# higher than the count of fields
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

PASSWORD_RESET_TIMEOUT_DAYS = 2
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


AXES_ONLY_USER_FAILURES = True

AXES_ONLY_ADMIN_SITE = True

AXES_COOLOFF_TIME = timedelta(minutes=10)

DAPP_KEY = env.str('DAPP_KEY', "f2338337-61ee-4eb6-8ea3-7c10b002d3f9")
DAPP_SECRET = env.str('DAPP_SECRET',
                      "0f8d831dddfac45b0ae56e0cadb92a293f39adbd5d957519cbbca22e37ab2173")

if SITE == "local":
    idle_time = 120
    AXES_FAILURE_LIMIT = 10
    INSTALLED_APPS.remove('multi_captcha_admin')
elif SITE == "stage":
    idle_time = 30
    AXES_FAILURE_LIMIT = 5
elif SITE == "test":
    idle_time = 5
    AXES_FAILURE_LIMIT = 5
elif SITE == "prod":
    AWS_STORAGE_BUCKET_NAME = 'inguz-prod'
    idle_time = 5
    AXES_FAILURE_LIMIT = 5

AUTO_LOGOUT = {
    'IDLE_TIME': timedelta(minutes=idle_time),
    'SESSION_TIME': timedelta(hours=8),
    'MESSAGE': 'Tu sesión ha expirado, por favor inicia sesión nuevamente.',
    'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
}

PREFIJO_CUENTA_INGUZ = "6461802180"

AXES_LOCKOUT_CALLABLE = "cactus.customAuthBackend.lockout"

URL_IMAGEN = "https://phototest420.s3.amazonaws.com/docs/docs/banca/comprobantes/comprobante_ejemplo.jpeg"

UBCUBO_USER = 'apiInvercratoSand'
UBCUBO_PWD = '258onttsR-3'
UBCUBO_KEY = 'KYC-kmhwgO5hJzyMYjty06Oqu1NIQV1-2Pyy'
UBCUBO_ENTIDAD = 5501
