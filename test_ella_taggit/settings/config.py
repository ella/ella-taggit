ADMINS = ()
MANAGERS = ADMINS

DEBUG = False
TEMPLATE_DEBUG = DEBUG
DISABLE_CACHE_TEMPLATE = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

TIME_ZONE = 'Europe/Prague'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# Make this unique, and don't share it with anybody.
SECRET_KEY = '88b-01asdlk329478(&^#$Q#l234%&:ASDk@#$'

# we want to reset whole cache in test
# until we do that, don't use cache
CACHE_BACKEND = 'dummy://'

