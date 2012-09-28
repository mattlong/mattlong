import os, json

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

IS_PRODUCTION = os.environ.get('MATTLONG_ORG_PRODUCTION') == 'true'

TEMPLATE_DEBUG = \
DEBUG = not IS_PRODUCTION

MANAGERS = ADMINS = (('Matt Long', 'matt@mattlong.org'),)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mattlongweb/defaultdb',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
USE_TZ = True

SECRET_KEY = '2d*1aum8)r9gcyd*m)vm=-)b#4!#2&amp;g!#@=o6#k+h2uqy$1*6o'

MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'

STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'toolbox.middleware.LogUnhandledExceptions',
)

ROOT_URLCONF = 'mattlongweb.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mattlongweb.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'mattlongweb/templates'),
)

INSTALLED_APPS = (
    #django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.markup',

    #thirdparty
    'south',

    #mine
    'toolbox',
    'base',
    'blog',
    'music',
    'bookmarks',
)

AUTH_PROFILE_MODULE = 'base.models.UserProfile'

OAUTH_EMAIL_MAP = json.loads(os.environ.get('OAUTH_EMAIL_MAP', '{}'))
OAUTH_DEBUG_CODE = None
OAUTH_DEBUG_ACCESS_TOKEN = None
GOOGLE_API_CLIENT_ID = os.environ.get('GOOGLE_API_CLIENT_ID')
GOOGLE_API_CLIENT_SECRET = os.environ.get('GOOGLE_API_CLIENT_SECRET')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        '': {
            'handlers': ['stdout'],
            'level': 'ERROR',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

if IS_PRODUCTION:
    SECRET_KEY = os.environ['MATTLONG_ORG_SECRET_KEY']
    STATIC_ROOT = os.environ['MATTLONG_ORG_STATIC_PATH']
    STATIC_URL = '//static.mattlong.org/'
    DATABASES['default']['NAME'] = '/etc/mattlong.org/defaultdb'

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INTERNAL_IPS = ('127.0.0.1',)
    DEBUG_TOOLBAR_CONFIG = {
        'HIDE_DJANGO_SQL': True,
        'ENABLE_STACKTRACES': False,
        'INTERCEPT_REDIRECTS': False,
    }
    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        #'debug_toolbar.panels.logger.LoggingPanel',
    )
    OAUTH_DEBUG_CODE = os.environ.get('OAUTH_DEBUG_CODE')
    OAUTH_DEBUG_ACCESS_TOKEN = os.environ.get('OAUTH_DEBUG_ACCESS_TOKEN')
