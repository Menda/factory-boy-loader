"""
Settings for tests.
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'example.sqlite',
    },
}


INSTALLED_APPS = [
    'tests.django_app'
]

MIDDLEWARE_CLASSES = ()

SECRET_KEY = 'testing.'
