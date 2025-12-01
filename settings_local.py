# tracking/settings_local.py
from tracking.settings import *

# Override production settings for local development
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
SECRET_KEY = 'django-insecure-local-dev-key-change-this-for-local-use-only'

# Turn off HTTPS for local development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0