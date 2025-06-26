from pathlib import Path

# -------------------------------------
# Base project path
# -------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------
# Security Settings
# -------------------------------------
SECRET_KEY = 'dummy-secret-key'  # 🔐 Replace this with a real secret in production
DEBUG = True
ALLOWED_HOSTS = ['whitelegacy-1.onrender.com', 'localhost', '127.0.0.1']


# -------------------------------------
# Installed Apps
# -------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Your app
    'dairyapp',
]

# -------------------------------------
# Middleware
# -------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# -------------------------------------
# URL Configuration
# -------------------------------------
ROOT_URLCONF = 'milkapp_project.urls'

# -------------------------------------
# Templates
# -------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # You can add global template paths here if needed
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

# -------------------------------------
# WSGI Application
# -------------------------------------
WSGI_APPLICATION = 'milkapp_project.wsgi.application'

# -------------------------------------
# Database
# -------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -------------------------------------
# Password Validation (optional)
# -------------------------------------
AUTH_PASSWORD_VALIDATORS = []

# -------------------------------------
# Localization
# -------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# -------------------------------------
# Static Files (CSS, JS, Images)
# -------------------------------------


# -------------------------------------
# Default Primary Key Field Type
# -------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------------
# Custom Login URL (required for @login_required)
# -------------------------------------
LOGIN_URL = '/login/'
# settings.py

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'dairyapp' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'  # <-- हे line add कर
