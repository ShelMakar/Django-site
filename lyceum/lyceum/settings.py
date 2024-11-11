import os
import pathlib

import django.utils.translation
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'base_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG_ENV = os.getenv('DJANGO_DEBUG', 'false').lower()
DEBUG = DEBUG_ENV in ('true', 'yes', '1', 'y', 't')

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')

ALLOW_REVERSE_ENV = os.getenv('DJANGO_ALLOW_REVERSE', 'true').lower()
ALLOW_REVERSE = ALLOW_REVERSE_ENV in (
    '',
    'true',
    'True',
    'yes',
    'YES',
    '1',
    'y',
)

DEFAULT_USER_IS_ACTIVE = os.getenv('DJANGO_DEFAULT_USER_IS_ACTIVE')

if DEFAULT_USER_IS_ACTIVE is None:
    DEFAULT_USER_IS_ACTIVE = DEBUG
else:
    DEFAULT_USER_IS_ACTIVE = DEFAULT_USER_IS_ACTIVE.lower() in ('true', '1')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'about.apps.AboutConfig',
    'catalog.apps.CatalogConfig',
    'core.apps.CoreConfig',
    'download.apps.DownloadConfig',
    'feedback.apps.FeedbackConfig',
    'homepage.apps.HomepageConfig',
    'users.apps.UsersConfig',
    'django_cleanup.apps.CleanupConfig',
    'django_ckeditor_5',
    'sorl.thumbnail',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'lyceum.middleware.Middleware',
]

if DEBUG:
    MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)
    INTERNAL_IPS = [
        '127.0.0.1',
    ]

ROOT_URLCONF = 'lyceum.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'lyceum.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.NumericPasswordValidator'
        ),
    },
]
LOGIN_URL = '/auth/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/auth/login/'

DEFAULT_USER_IS_ACTIVE = os.getenv('DJANGO_DEFAULT_USER_IS_ACTIVE', 'true')
LOCALE_PATHS = [BASE_DIR / 'locale']

LANGUAGE_CODE = 'ru'
LANGUAGES = [
    ('ru', django.utils.translation.gettext_lazy('Русский')),
    ('en', django.utils.translation.gettext_lazy('Английский')),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static_dev',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

custom_color_palette = [
    {
        'color': 'hsl(4, 90%, 58%)',
        'label': 'Red',
    },
    {
        'color': 'hsl(340, 82%, 52%)',
        'label': 'Pink',
    },
    {
        'color': 'hsl(291, 64%, 42%)',
        'label': 'Purple',
    },
    {
        'color': 'hsl(262, 52%, 47%)',
        'label': 'Deep Purple',
    },
    {
        'color': 'hsl(231, 48%, 48%)',
        'label': 'Indigo',
    },
    {
        'color': 'hsl(207, 90%, 54%)',
        'label': 'Blue',
    },
]

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading',
            '|',
            'bold',
            'italic',
            'link',
            'bulletedList',
            'numberedList',
            'blockQuote',
            'imageUpload',
            'Table',
            'alignment:left',
            'alignment:center',
            'alignment:right',
            'alignment:justify',
            'font',
            'fontSize',
            'textColor',
            'outdent',
            'indent',
            'horizontalRule',
        ],
        'alignment': {'options': ['left', 'right', 'center', 'justify']},
    },
    'extends': {
        'blockToolbar': [
            'paragraph',
            'heading1',
            'heading2',
            'heading3',
            '|',
            'bulletedList',
            'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': [
            'heading',
            '|',
            'outdent',
            'indent',
            '|',
            'bold',
            'italic',
            'link',
            'underline',
            'strikethrough',
            'code',
            'subscript',
            'superscript',
            'highlight',
            '|',
            'codeBlock',
            'sourceEditing',
            'insertImage',
            'bulletedList',
            'numberedList',
            'todoList',
            '|',
            'blockQuote',
            'imageUpload',
            '|',
            'fontSize',
            'fontFamily',
            'fontColor',
            'fontBackgroundColor',
            'mediaEmbed',
            'removeFormat',
            'insertTable',
            'alignment:left',
            'alignment:center',
            'alignment:right',
            'alignment:justify',
        ],
        'image': {
            'toolbar': [
                'imageTextAlternative',
                '|',
                'imageStyle:alignLeft',
                'imageStyle:alignRight',
                'imageStyle:alignCenter',
                'imageStyle:side',
                '|',
            ],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ],
        },
        'table': {
            'contentToolbar': [
                'tableColumn',
                'tableRow',
                'mergeTableCells',
                'tableProperties',
                'tableCellProperties',
            ],
            'tableProperties': {
                'borderColors': custom_color_palette,
                'backgroundColors': custom_color_palette,
            },
            'tableCellProperties': {
                'borderColors': custom_color_palette,
                'backgroundColors': custom_color_palette,
            },
        },
        'heading': {
            'options': [
                {
                    'model': 'paragraph',
                    'title': 'Paragraph',
                    'class': 'ck-heading_paragraph',
                },
                {
                    'model': 'heading1',
                    'view': 'h1',
                    'title': 'Heading 1',
                    'class': 'ck-heading_heading1',
                },
                {
                    'model': 'heading2',
                    'view': 'h2',
                    'title': 'Heading 2',
                    'class': 'ck-heading_heading2',
                },
                {
                    'model': 'heading3',
                    'view': 'h3',
                    'title': 'Heading 3',
                    'class': 'ck-heading_heading3',
                },
            ],
        },
    },
    'list': {
        'properties': {
            'styles': 'true',
            'startIndex': 'true',
            'reversed': 'true',
        },
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

EMAIL_FILE_PATH = BASE_DIR / 'send_mail'

DEFAULT_FROM_EMAIL = os.getenv('DJANGO_MAIL', 'makarmolodec@mail.ru')
