# default config
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = "secret_key"
    CASSANDRA_HOSTS = ['127.0.0.1']
    CASSANDRA_KEYSPACE = 'SBS'
