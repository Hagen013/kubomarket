import os
import environ
from kombu import Queue, Exchange


env = environ.Env()
env.read_env()


# ROUTING
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'
# ROUTING END


# PATHS
# ------------------------------------------------------------------------------
ROOT_DIR = environ.Path(__file__) - 4  # (web/backend/config/settings/base.py - 4 = web/)
# PATHS END


# SECURITY SETINGS
# ------------------------------------------------------------------------------
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SECURITY SETINGS END


# APPLICATIONS CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
]

THIRD_PARTY_APPS = [
    'django_extensions',
    'polymorphic',
    'mptt',
    'rest_framework',
    'imagekit',
    'django_redis',
    'jsoneditor',
    'raven.contrib.django.raven_compat',
    'social_django',
]

LOCAL_APPS = [
    'cart',
    'api',
    'core',
    'shop_cubes',
    'controls',
    'users'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
# APPLICATIONS CONFIGURATION END

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SOCIAL_AUTH_LOGIN_ERROR_URL = "/u/registration/?from=oauth"

# LOADERS CONFIGURATION
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            '../frontend/templates/',
        ],
        'OPTIONS': {
            'environment': 'config.jinja2env.environment',
        }
    },
]


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    str(ROOT_DIR.path('frontend/static')),
)

# MAIL SETTINGS
# ------------------------------------------------------------------------------
EMAIL_HOST_USER = env("DJANGO_EMAIL_HOST_USER")
DEFAULT_FROM_EMAIL = env("DJANGO_DEFAULT_FROM_EMAIL")
EMAIL_PORT = int(env("DJANGO_EMAIL_PORT"))
EMAIL_HOST = env("DJANGO_EMAIL_HOST")
EMAIL_HOST_PASSWORD = env("DJANGO_EMAIL_HOST_PASSWORD")
EMAIL_USE_SSL = True

# REDIS SETTINGS
# ------------------------------------------------------------------------------
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_HOST = "redis"


# RABBIT SETTINGS
# ------------------------------------------------------------------------------
RABBIT_HOSTNAME = "rabbit"
RABBIT_USER = os.environ.get('RABBIT_USER', 'RABBIT_USER')
RABBIT_PASS = os.environ.get('RABBIT_PASS', 'RABBIT_PASS')
RABBIT_VHOST = os.environ.get('RABBIT_VHOST', 'RABBIT_VHOST')

BROKER_URL = 'amqp://{user}:{password}@{hostname}/{vhost}'.format(
    user=RABBIT_USER,
    password=RABBIT_PASS,
    hostname=RABBIT_HOSTNAME,
    vhost=RABBIT_VHOST,
)


# We don't want to have dead connections stored on rabbitmq,
# so we have to negotiate using heartbeats

BROKER_HEARTBEAT = '?heartbeat=30'

if not BROKER_URL.endswith(BROKER_HEARTBEAT):
    BROKER_URL += BROKER_HEARTBEAT
BROKER_POOL_LIMIT = 10
BROKER_CONNECTION_TIMEOUT = 10


# CELERY SETTINGS
# ------------------------------------------------------------------------------
CELERY_RESULT_BACKEND = 'redis://%s:%d/%d' % (REDIS_HOST, REDIS_PORT, REDIS_DB)
CELERY_IMPORTS = (
    'tasks.elastic',
    'tasks.mail_notifications',
    'tasks.yandex_market',
    'tasks.mywarehouse',
    'tasks.controls',
    'tasks.images',
    'tasks.asist',
)

CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('media', Exchange('media'), routing_key='media')
)
CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_ROUTING_KEY = 'default'
CELERY_ROUTES = {
    'tasks.images.synchronize_images': {'queue': 'media'},
    'tasks.images.process_media_url': {'queue': 'media'},
    'tasks.add_cubes_image_from_file': {'queue': 'media'},
    'tasks.set_cubes_images_order': {'queue': 'media'}
}

CELERY_REDIS_MAX_CONNECTIONS = 8
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_ALWAYS_EAGER = False
CELERY_IGNORE_RESULT = False
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'Europe/Moscow'


# ELASTICSEARCH SETTINGS
# ------------------------------------------------------------------------------
ELASTICSEARCH_HOST = 'elasticsearch'
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_URL = 'http://{0}:{1}/'.format(ELASTICSEARCH_HOST, ELASTICSEARCH_PORT)
ELASTICSEARCH_SNAPSHOT_REPO = 'backups'
ELASTICSEARCH_SNAPSHOT_NAME = 'backup'
ELASTICSEARCH_SNAPSHOT_DIR = '/var/graph_market/elastic-snapshots/'


# REST FRAMEWORK
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    # )
}

MYWAREHOUSE_CUBES_STORE = os.environ.get('MYWAREHOUSE_CUBES_STORE')
MYWAREHOUSE_LOGIN = os.environ.get('MYWAREHOUSE_LOGIN')
MYWAREHOUSE_PASSWORD = os.environ.get('MYWAREHOUSE_PASSWORD')

# SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"

MERCHANT_ID = os.environ.get('MERCHANT_ID')
MERCHANT_LOGIN = os.environ.get('MERCHANT_LOGIN')
MERCHANT_PASSWORD = os.environ.get('MERCHANT_PASSWORD')

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.odnoklassniki.OdnoklassnikiOAuth2',
    'social_core.backends.yandex.YandexOAuth2',
    'social_core.backends.mailru.MailruOAuth2',
    'django.contrib.auth.backends.ModelBackend'
)

SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "762613105757-jtabi7drco03vihfpcp1pa5mf5fma840.apps.googleusercontent.com"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "u0GwqHTUTU5TfYAum-JyUlE8"

SOCIAL_AUTH_VK_OAUTH2_KEY = '6623041'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'M06QPdwbD4v6NkgmxKlu'
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ["email", ]

SOCIAL_AUTH_MAILRU_OAUTH2_KEY = '760828'
SOCIAL_AUTH_MAILRU_OAUTH2_SECRET = '47539eeb16e3e07bb9ad337e506d74ca'

SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_KEY = '1268317184'
SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_SECRET = '057EFAAE12B743FD8A0BABBD'
SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_PUBLIC_NAME = 'CBANPJJMEBABABABA'
# SOCIAL_AUTH_ODNOKLASSNIKI_APP_EXTRA_USER_DATA_LIST = "('email',)"

SOCIAL_AUTH_YANDEX_OAUTH2_KEY = 'd347e0755feb4f68845e68a314e39d93'
SOCIAL_AUTH_YANDEX_OAUTH2_SECRET = '5922a32bea3747b081d08715e0d47889'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'config.programm1.registrate_user',
    'social_core.pipeline.social_auth.associate_user',
)
