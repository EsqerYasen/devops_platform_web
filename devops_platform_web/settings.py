"""
Django settings for devops_web project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6vxuw+&sqct(*0aa5r$3wtfk&lludc(19g1vzax5lfvuy23vvn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'common',
    'common_platform',
    'devops_cmdb',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.FilterGroup.Filter'
]

ROOT_URLCONF = 'devops_platform_web.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'devops_platform_web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'devops_web',
    #     'USER': 'root',
    #     'PASSWORD': 'mysql1234',
    #     'HOST': 'localhost',
    #     'PORT': '3306',
    #     'OPTIONS': {
    #         'init_command': 'SET default_storage_engine=INNODB',
    #     },
    # }
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'devops_workshop_dev_web',
    #     'USER': 'root',
    #     'PASSWORD': 'devops',
    #     'HOST': '172.29.164.91',
    #     'PORT': '3306',
    #     'OPTIONS': {
    #         'init_command': 'SET default_storage_engine=INNODB',
    #     },
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'devops_workshop_prod_web',
        'USER': 'root',
        'PASSWORD': 'devops',
        'HOST': '172.17.144.150',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': 'SET default_storage_engine=INNODB',
        },
    }
}


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

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static/'

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, "saltops-web/dist/static"),
    ('scripts', os.path.join(STATIC_ROOT, 'scripts').replace('\\', '/')),
    ('asserts', os.path.join(STATIC_ROOT, 'asserts').replace('\\', '/')),
    ('hplus', os.path.join(STATIC_ROOT, 'hplus').replace('\\', '/')),
    ('admin', os.path.join(STATIC_ROOT, 'admin').replace('\\', '/')),
    ('djcelery', os.path.join(STATIC_ROOT, 'djcelery').replace('\\', '/')),
    ('js', os.path.join(STATIC_ROOT, 'js').replace('\\', '/')),
    ('mptt', os.path.join(STATIC_ROOT, 'mptt').replace('\\', '/')),
    ('range_filter', os.path.join(STATIC_ROOT, 'range_filter').replace('\\', '/')),
    ('rest_framework', os.path.join(STATIC_ROOT, 'rest_framework').replace('\\', '/')),
    ('codemirror', os.path.join(STATIC_ROOT, 'codemirror').replace('\\', '/')),
)


REST_API_CONFIG = {
        #本地
        # 'cmdb': {
        #     'ip_prot': '172.29.164.92:8000'
        # },
        # 'job':{
        #     'ip_prot': '172.29.164.92:8001'
        # }
        #生产
        'cmdb': {
            'ip_prot': '172.17.144.150:8000'
        },
        'job': {
            'ip_prot': '172.17.144.150:8001'
        }
    }


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] [%(levelname)s] [%(module)s] [process:%(process)d] [thread:%(thread)d] %(message)s'
        },
    },
    'handlers': {
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR+'/logs/','devops_web.log'),
            'maxBytes': 1024*1024*50,
            'backupCount': 10,
            'formatter': 'verbose'
        },
        'console':{
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'devops_platform_log': {
            'handlers': ['error', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

LOGIN_URL = "/"

PER_PAGE = 10

UPLOAD_SCRIPT_PATH = "/opt/devops/filetrunk/"