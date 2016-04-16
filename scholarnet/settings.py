"""
Django settings for scholarnet project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os import path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = path.dirname(path.abspath(path.dirname(__file__)))
TEMPLATE_PATH = os.path.join(PROJECT_ROOT, 'app/templates')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ymr!=&e-wd2z*-^@zxpu6#3s!e7^0kheq)j$cdd!b^8$y08c^p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG
ADMINS = (
 ('Daniel Kindimba', 'daniellykindimba@gmail.com'),
 ('Emmanuel Meena', 'mcamocci@gmail.com'),
 ('Walter Kimaro', 'waky07@gmail.com'),
)
ALLOWED_HOSTS = ['www.scholarnetapp.com','scholarnetapp.com']

SITE_ID = 1
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.redirects',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'endless_pagination',
    'app',
    'mob',
    'manager',
    'storages',
    'corsheaders',
    'tastypie',
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_PATH],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.tz',
            ],
        },
    },
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsPostCsrfMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'middleware.crossdomainxhr.XsSharing',
    'django.middleware.security.SecurityMiddleware',
)

X_FRAME_OPTIONS = 'DENY'

ROOT_URLCONF = 'scholarnet.urls'

WSGI_APPLICATION = 'scholarnet.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Dar_es_Salaam'

USE_I18N = True

USE_L10N = True

USE_TZ = False




#setting the python memcached
CACHES = {
    'default':{
        'BACKEND':'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION':'localhost:8000',
        }
    }
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_ROOT = path.join(PROJECT_ROOT, 'static').replace('\\', '/')

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '..', 'app/static').replace('\\','/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

ADMIN_SITE_HEADER = 'ScholarNet Adminstrator Management Panel'
ADMIN_SITE_TITLE = 'ScholarNet'


from django.core.urlresolvers import reverse_lazy
LOGIN_URL = reverse_lazy('login')
LOGOUT_URL = reverse_lazy('logout')
LOGIN_REDIRECT_URL = "/app/home/"


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },

    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
     'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

APPEND_SLASH = False


ENDLESS_PAGINATION_PAGE_LIST_CALLABLE = True
ENDLESS_PAGINATION_PREVIOUS_LABEL = '<'
ENDLESS_PAGINATION_NEXT_LABEL = '>'
ENDLESS_PAGINATION_FIRST_LABEL = '<<'
ENDLESS_PAGINATION_LAST_LABEL = '>>'
ENDLESS_PAGINATION_DEFAULT_CALLABLE_EXTREMES = 15
ENDLESS_PAGINATION_DEFAULT_CALLABLE_AROUNDS = 15

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)

CORS_ORIGIN_WHITELIST = (
'scholarnetapp.com'
)

CSRF_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

API_LIMIT_PER_PAGE = 50
TASTYPIE_FULL_DEBUG = True
TASTYPIE_CANNED_ERROR = "Oops, we broke it!"
TASTYPIE_DEFAULT_FORMATS = ['json', 'xml', 'yaml', 'plist']
TASTYPIE_ABSTRACT_APIKEY = False
