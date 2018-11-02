# default config
from datetime import timedelta


class BaseConfig(object):
    DEBUG = False  # by default do not load debug mode
    # secret key for database. Todo: change it
    SECRET_KEY = "9u23hghhfeuhf0gbgrijwdaf32hf02ugt3h"
    SITE_KEY = "6LcSb3cUAAAAAF8NkmVESlCeODt-7F9qUmYaqKXy"
    CASSANDRA_HOSTS = ['127.0.0.1']  # list of cassandra cluster IP addresses.
    CASSANDRA_KEYSPACE = "SBS"  # name of the keyspace (database)
    # PERMANENT_SESSION_LIFETIME = timedelta(minutes=1)


class DevelopmentConfig(BaseConfig):
    DEBUG = True
