# import json
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT_DIR = os.path.dirname(BASE_DIR)
STATIC_DIR = os.path.join(ROOT_DIR, '.static')
SECRET_DIR = os.path.join(ROOT_DIR, '.secrets')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

secrets = json.load(open(os.path.join(SECRET_DIR, 'base.json')))
SECRET_KEY = secrets['SECRET_KEY']

# social login secret key - .secret
FACEBOOK_APP_ID = secrets["FACEBOOK_APP_ID"]
FACEBOOK_APP_SECRET = secrets["FACEBOOK_APP_SECRET"]
KAKAO_APP_ID = secrets['KAKAO_APP_ID']
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ROOT_DIR, ".media")

STATIC_URL = '/static/'

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATICFILES_DIRS = [
    os.path.join(ROOT_DIR, '.static/admin'),
]

# Auth
AUTH_USER_MODEL = 'members.Users'

#  django deeg toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]


CORS_ORIGIN_WHITELIST = (
    '127.0.0.1',
    'localhost:3004',
)
INSTALLED_APPS = [
    # apps
    'members',
    'posts.apps.PostsConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third part package
    'django_extensions',
    'corsheaders',
    'debug_toolbar',
    'django_filters',
    'sslserver',
    'rest_framework',
    'rest_framework.authtoken',

    # django 는 밑에서부터 위로 컴파일
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.FormParser',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    # 'config.middleware.CORSMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',

]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATES_DIR,
        ],
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

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # <- 디폴트 모델 백엔드
    'members.backends.FacebookBackend',

)

SITE_ID = 1  # 사이트 아이디 기본값
# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True
