"""
Django settings for simedarby project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import datetime
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY','4ef4+af)ifk#vgvk&055^djs(4jml-h3@q1$k(hcqb)u9t@n7i')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG',True)

ALLOWED_HOSTS = ['*']

CSRF_COOKIE_SAMESITE = None
X_FRAME_OPTIONS = 'ALLOW-FROM *'
# Application definition

INSTALLED_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ordered_model',
    'djmoney',
    'tinymce',
    'rest_framework',
    'rest_framework.pagination',
    'django_filters',
    'corsheaders',
    'drf_yasg',
    'crispy_forms',
    'smart_selects',
    #'easyaudit',
    'rangefilter',
    'users.apps.UsersConfig',
    'residents.apps.ResidentsConfig',
    'announcements.apps.AnnouncementsConfig',
    'security_guards.apps.SecurityGuardsConfig',
    'billings.apps.BillingsConfig',
    'ivms.apps.IvmsConfig',
    'reports.apps.ReportsConfig',
    'visitors.apps.VisitorsConfig',
    'notification.apps.NotificationConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    #'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'simedarby.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'simedarby.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
#mysql
if(DEBUG):
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', #django.db.backends.mysql 
            'NAME': os.environ['MYSQL_DBNAME'], #local: libraries #server: 
            'USER': os.environ['MYSQL_USERNAME'], #root #root
            'PASSWORD': os.environ['MYSQL_PASSWORD'], #local: root #server: 
            'HOST': os.environ['MYSQL_HOSTNAME'], #local: localhost  #server:
            'PORT': '3306',
            'OPTIONS': {
                'ssl': {
                    'cert':'/static/BaltimoreCyberTrustRoot.crt.pem' ,
                }
            },
        }
    }



# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS',"redis://127.0.0.1:6379/0"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kuala_Lumpur'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
CRISPY_TEMPLATE_PACK = 'bootstrap3'
DJANGO_EASY_AUDIT_UNREGISTERED_URLS_DEFAULT = [r'^/admin/', r'^/static/', r'^/favicon.ico$', r'/jet/',r'/tinymce/',r'/media/']
SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
        'JWT': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (

       'security_guards.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'security_guards.permissions.IsAuthenticated', ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DATETIME_FORMAT': "%d-%m-%Y %I:%M %p",
}
JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'api.jwt_login.jwt_response_payload_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=365),
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': 'HS256',
    'JWT_ALLOW_REFRESH': True,
}
STATIC_ROOT = os.environ.get('STATIC_PATH',"./static_files/")

STATICFILES_DIRS = [
    
    os.environ.get('STATIC_PATH',"./static/"), 
]
#email config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'simedarbyvms8@gmail.com'
EMAIL_HOST_PASSWORD = 'simedarby112211'
EMAIL_PORT = 587
MEDIA_URL = '/media/'
MEDIA_ROOT = os.environ.get('MEDIA_PATH',"./media_storage/")
PASSWORD_RESET_TIMEOUT_DAYS = 0.5
CORS_ORIGIN_ALLOW_ALL = True
AUTH_USER_MODEL = 'users.User'
PHONENUMBER_DEFAULT_REGION = "MY"
USE_DJANGO_JQUERY = True
JQUERY_URL = False
JET_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'
JET_SIDE_MENU_COMPACT = False
JET_DEFAULT_THEME = 'simedarby'
JET_APPLICATION_PAGE = False
JET_LOGO = "/ivms/img/simedarby-logo.svg"
JET_LOGO_WIDTH = "50%"
JET_LOGO_HEIGHT = "50%"
JET_LOGIN_LOGO = "/ivms/img/simedarby-logo_blk.svg"
JET_LOGIN_LOGO_WIDTH = "50%"
JET_LOGIN_LOGO_HEIGHT = "50%"
JET_LOGIN_BACKGROUND = "url('"+STATIC_URL+"/ivms/img/gallery-glades.jpg')"
TINYMCE_DEFAULT_CONFIG = {
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': 'link image preview codesample contextmenu table code lists',
    'toolbar1': 'formatselect | bold italic underline | alignleft aligncenter alignright alignjustify '
               '| bullist numlist | outdent indent | table | link image | codesample | preview code',
    'contextmenu': 'formats | link image',
    'menubar': False,
    'inline': False,
    'statusbar': True,
    'width': 'auto',
    'height': 360,
    'default_link_target':"_blank",
    'link_class_list': [
        {'title': 'External Link', 'value': 'external'}
     ],
    'image_dimensions': False,
    'image_class_list': [
    {'title': 'Responsive', 'value': 'img-responsive'},
  ]
}
JET_SIDE_MENU_ITEMS = [
    {'app_label': 'announcements', 'items': [
        {'name': 'announcement'},
    ]},
    {'app_label': 'billings', 'items': [
        {'name': 'billtype','permissions': ['billings.change_billtype']},
        {'name': 'billsetting'},
        {'name': 'invoice'},
    ]},
    {'app_label': 'residents', 'items': [
        {'name': 'community','permissions': ['residents.change_community']},
        {'name': 'area','permissions': ['residents.change_area']},
        {'name': 'street','permissions': ['residents.change_street']},
        {'name': 'lot','permissions': ['residents.change_lot']},
        {'name': 'resident','permissions': ['residents.change_resident']},
        {'name': 'request','permissions': ['residents.change_request']},
        {'name': 'requestfamily','permissions': ['residents.change_requestfamily']},
    ]},
    {'app_label': 'security_guards', 'items': [
        {'name': 'security','permissions': ['security_guards.change_security']},
        {'name': 'reasonsetting','permissions': ['security_guards.change_reasonsetting']},
         {'name': 'devicenumber','permissions': ['security_guards.change_devicenumber']},
        {'name': 'passnumber','permissions': ['security_guards.change_passnumber']},
    ],'permissions': ['security_guards.change_security']},
    {'app_label': 'ivms', 'items': [
        {'name': 'boomgate'},
        {'name': 'ipcamera'},
    ],'permissions': ['security_guards.change_security']},
    {'app_label': 'users', 'items': [
        {'name': 'user'},
    ],'permissions': ['core.user']},
    {'app_label': 'auth', 'items': [
        {'name': 'group'},
    ],'permissions': ['core.user']},

    {'app_label': 'reports', 'items': [
        {'name': 'invoicereport'},
        {'name': 'paymentreport'},
        {'name': 'visitreport'},
    ],},
]