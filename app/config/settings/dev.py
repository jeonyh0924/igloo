from .base import *

DEV_JSON = json.load(open(os.path.join(SECRET_DIR, 'dev.json')))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]


STATICFILES_DIRS = [
    STATIC_DIR,
]
secrets = json.load(open(os.path.join(SECRET_DIR, 'base.json')))
SECRET_KEY = secrets['SECRET_KEY']

WSGI_APPLICATION = 'config.wsgi.dev.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = DEV_JSON['DATABASES']

# DATABASES = {
#      'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
#     }
# }
