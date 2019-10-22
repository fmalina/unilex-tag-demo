from settings_local import *
import os.path

PWD = os.path.dirname(os.path.realpath(__file__))

CACHE_FOLDERS = ['fs']
DOMAIN = 'unilexicon.com'
SITE_URL = 'https://' + DOMAIN
ALLOWED_HOSTS = ['*', '127.0.0.1', DOMAIN]
DATABASES = {'default': {'ENGINE': 'django.contrib.gis.db.backends.mysql',
                         'NAME': 'fs', 'USER': DB_USER, 'PASSWORD': DB_PASS}}
MAPS_API_KEY = 'A'
TIME_ZONE = 'Europe/Paris'
DATE_INPUT_FORMATS = ['%d/%m/%Y']
DATE_FORMAT = "j. F Y"
LANGUAGE_CODE = 'en-gb'
USE_I18N = USE_L10N = False
DEFAULT_FROM_EMAIL = ADMIN_EMAIL
ADMINS = MANAGERS = [('Admin', ADMIN_EMAIL)]
PROJECT_ROOT = PWD.replace('apps', '')
STATIC_ROOT = PROJECT_ROOT + 'static/'
STATIC_URL = '/static/'
SITE_ID = 1
LOGIN_REDIRECT_URL = '/after_joining'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
AUTHENTICATION_BACKENDS = ['allauth.account.auth_backends.AuthenticationBackend']
UPLOAD_COLLECTION_MODEL = 'org.Org'
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = f'Fashion Sourcing <{ADMIN_EMAIL}>'

ROOT_URLCONF = 'urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [PROJECT_ROOT + 'apps/templates/'],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.contrib.messages.context_processors.messages',
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.debug',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.template.context_processors.request',
            'utils.more_context',
        ]
    }
}]
MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'utils.site_middleware',
)
INSTALLED_APPS = (
    'org',
    'product',
    'upload',
    'pay',
    'fs',
    'allauth',
    'emails',
    'easy_thumbnails',
    'django_messages',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django.contrib.humanize',
    'django.contrib.gis',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',
)
