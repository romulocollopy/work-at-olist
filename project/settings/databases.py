import decouple
from dj_database_url import parse as db_parse

from .base import BASE_DIR

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


DEFAULT_DATABASE_URL = decouple.config(
    'DATABASE_URL', default=str(
        'sqlite:///{}/phonebilling.sqlite'.format(BASE_DIR.parent)
    )
)

DATABASES = {
    'default': db_parse(DEFAULT_DATABASE_URL),
}
