SECRET_KEY = 'drfbatch'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

ROOT_URLCONF = 'tests.utils.app.urls'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'rest_framework',
    'drf_batch'
]

REST_FRAMEWORK = {
    'UNAUTHENTICATED_USER': None,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}
