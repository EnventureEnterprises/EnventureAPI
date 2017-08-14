import os
from os.path import join

from configurations import Configuration, values

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Common(Configuration):

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
          'django.contrib.gis',


        # Third party apps
        'rest_framework',  
                  # utilities for rest apis
        'rest_framework.authtoken',  # token authentication
        'django_rq',                 # asynchronous queuing   
         'versatileimagefield',   # image manipulation
        'rest_auth',
        'rest_auth.registration',
        'tagulous',
        'actstream',
           'mptt',
        'django_extensions',
         'rest_framework_gis',
        'oauth2_provider',
         'social.apps.django_app.default',
         'rest_framework_social_oauth2',
        'corsheaders',
        # Your apps
         'users',
        'authentication',
        'bootstrap3',

        'bookkeeping',
        'django_vanilla.django_vanilla',
       

    )

    # https://docs.djangoproject.com/en/1.8/topics/http/middleware/
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'users.middleware.LoggingMiddleware',
    )

    ROOT_URLCONF = 'urls'

    SECRET_KEY = 'Not a secret'
    WSGI_APPLICATION = 'wsgi.application'

    # Email
    EMAIL_BACKEND = values.Value('django.core.mail.backends.smtp.EmailBackend')

    MANAGERS = (
        ('Author', 'mugisha@sparkpl.ug'),
    )

    # Postgres
    DATABASES = values.DatabaseURLValue('postgres://localhost/urb')

    # General
    APPEND_SLASH = values.BooleanValue(False)
    TIME_ZONE = 'UTC'
    LANGUAGE_CODE = 'en-us'
    # If you set this to False, Django will make some optimizations so as not
    # to load the internationalization machinery.
    USE_I18N = False
    USE_L10N = True
    USE_TZ = True
    LOGIN_REDIRECT_URL = '/'

    # Static Files
    STATIC_ROOT = join(os.path.dirname(BASE_DIR), 'staticfiles')
    STATICFILES_DIRS = [join(os.path.dirname(BASE_DIR), 'static'), ]
    STATIC_URL = '/static/'
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    # Media files
    MEDIA_ROOT = join(os.path.dirname(BASE_DIR), 'media')
    MEDIA_URL = '/media/'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [STATICFILES_DIRS],
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                    'django.contrib.messages.context_processors.messages',
                    'django.template.context_processors.request',
                     'social.apps.django_app.context_processors.backends',
                     'social.apps.django_app.context_processors.login_redirect',

                ],
                'loaders':[
                    ('django.template.loaders.cached.Loader', [
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader',
                    ]),
                ],
            },
        },
    ]






    # Set DEBUG to False as a default for safety
    # https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = values.BooleanValue(False)
    for config in TEMPLATES:
        config['OPTIONS']['debug'] = DEBUG

    # Logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
            'rq_console': {
                'format': '%(asctime)s %(message)s',
                'datefmt': '%H:%M:%S',
            },
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'rq_console': {
                'level': 'DEBUG',
                'class': 'rq.utils.ColorizingStreamHandler',
                'formatter': 'rq_console',
                'exclude': ['%(asctime)s'],
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True
            },
            'rq.worker': {
                'handlers': ['rq_console'],
                'level': 'DEBUG'
            },
        }
    }

    # Custom user app
    AUTH_USER_MODEL = 'users.User'

    # Django Rest Framework
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 100,
        'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ),
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.AllowAny',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'oauth2_provider.ext.rest_framework.OAuth2Authentication',
            'rest_framework_social_oauth2.authentication.SocialAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.TokenAuthentication',
        ),
        'DEFAULT_PARSER_CLASSES': (
           'rest_framework.parsers.JSONParser',
          'rest_framework.parsers.FormParser',
          'rest_framework.parsers.MultiPartParser',
        ),
    }

    # Versatile Image Field
    VERSATILEIMAGEFIELD_SETTINGS = {
        # The amount of time, in seconds, that references to created images
        # should be stored in the cache. Defaults to `2592000` (30 days)
        'cache_length': 2592000,
        'cache_name': 'versatileimagefield_cache',
        'jpeg_resize_quality': 70,
        'sized_directory_name': '__sized__',
        'filtered_directory_name': '__filtered__',
        'placeholder_directory_name': '__placeholder__',
        'create_images_on_demand': False,
        'cache_name': 'versatileimagefield_cache',
        'cache_length': 2592000,
    }

    VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
        'image_gallery': [
            ('gallery_large', 'crop__800x450'),
            ('gallery_medium', 'crop__420x300'),
            ('gallery_square_small', 'crop__50x50')
        ],
        'primary_image_detail': [
            ('hero', 'crop__600x283'),
            ('social', 'thumbnail__800x800')
        ],
        'primary_image_list': [
            ('list', 'crop__400x225'),
        ],
        'headshot': [
            ('headshot_small', 'crop__150x175'),
        ]
        }

    AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'authentication.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
     'rest_framework_social_oauth2.backends.DjangoOAuth2',
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.facebook.FacebookOAuth2',
   )
    SITE_ID = 1
    

    SOCIAL_AUTH_FACEBOOK_SCOPE = ['email','user_friends','public_profile']
    SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email,first_name,last_name,gender,cover'
    }

    SERIALIZATION_MODULES = {
    'xml':    'tagulous.serializers.xml_serializer',
    'json':   'tagulous.serializers.json',
    'python': 'tagulous.serializers.python',
    'yaml':   'tagulous.serializers.pyyaml',
    }

    SOCIAL_AUTH_PIPELINE = (

    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'users.pipeline.get_avatar', # This is a path of your pipeline.py
    #and get_avatar is the function.
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'VERBOSE',  # change debug level as appropiate
            'propagate': True,
        },
    },
}


