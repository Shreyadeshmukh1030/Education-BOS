from .base import *

DEBUG = False

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# Ensure DATABASE_URL is required in production
DATABASES = {
    'default': env.db('DATABASE_URL')
}

# Production specific security settings
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True

# You might want to configure CSRF_COOKIE_SECURE and SESSION_COOKIE_SECURE based on HTTPS
# SECURE_SSL_REDIRECT = True
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
