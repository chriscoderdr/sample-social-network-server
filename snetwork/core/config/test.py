import os
# Testing Config: Begin
DEBUG = True
TESTING = False
SECRET_KEY = 'oqmNk8leNYaKH3ns'
PREFERRED_URL_SCHEME = 'https'
SQLALCHEMY_ECHO = False
# Testing Config: End

SQLALCHEMY_DATABASE_URI = ("postgresql://snetworkdba"
                           ":elcj2304@localhost/snetwork")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SERVER_NAME = 'localhost:5000'
CACHE_TYPE = 'redis'
CACHE_KEY_PREFIX = 'snetwork_'
CACHE_REDIS_URL = 'redis://localhost:6379'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'
SECURITY_PASSWORD_SALT = 'oqmNk8leNYaKH3ns'
