from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_URLCONF = 'fintrack_project.urls'

# ===================== STATIC & MEDIA =====================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ===================== SECRET & DEBUG =====================
SECRET_KEY = os.environ.get('SECRET_KEY', 'TEBGALI@49360602')
DEBUG =  'True'
ALLOWED_HOSTS = ['*']

# ===================== DATABASE =====================
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        ssl_require=False,
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"  # fallback for local dev
    )
}

# ===================== APPS =====================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'crispy_forms',
    'crispy_bootstrap4',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django.contrib.sites',

    # Local apps
    'users',
    'finance',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'
SITE_ID = 1

# ===================== AUTH =====================
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300

LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = '/finance/dashboard/' 
LOGOUT_REDIRECT_URL = 'account_login'

# ===================== EMAIL (Gmail SMTP) =====================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '19263@isms.esp.mr'
EMAIL_HOST_PASSWORD = 'goaprxlsjqjmrqhn'
DEFAULT_FROM_EMAIL = f'FinTrack+ <{EMAIL_HOST_USER}>'

# ===================== MIDDLEWARE =====================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # REQUIRED for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# ===================== TEMPLATES =====================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # REQUIRED by allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fintrack_project.wsgi.application'

# ===================== PASSWORD VALIDATORS =====================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ===================== INTERNATIONALIZATION =====================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ===================== DEFAULT PRIMARY KEY FIELD TYPE =====================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = ['https://fintrack-project.onrender.com']