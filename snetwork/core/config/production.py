DEBUG = True
TESTING = False
SECRET_KEY = "Hg*Li8sNgb8Xd3%XtgP)48bAKVVHCW"
PREFERRED_URL_SCHEME = 'https'

SQLALCHEMY_DATABASE_URI = ("postgresql://snetworkdba"
                           ":elcj2304@localhost/snetwork")
SQLALCHEMY_TRACK_MODIFICATIONS = False

SERVER_NAME = 'cristiangomez.me'
CACHE_TYPE = 'redis'
CACHE_KEY_PREFIX = 'snetwork_'
CACHE_REDIS_URL = 'redis://localhost:6379'
SECURITY_PASSWORD_SALT = 'oqmNk8leNYaKH3ns'
