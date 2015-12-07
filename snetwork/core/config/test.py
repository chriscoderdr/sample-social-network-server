# Testing Config: Begin
DEBUG = True
TESTING = True
SECRET_KEY = "Hg*Li8sNgb8Xd3%XtgP)48bAKVVHCW"
PREFERRED_URL_SCHEME = 'https'
SQLALCHEMY_ECHO = True
# Testing Config: End

SQLALCHEMY_DATABASE_URI = ("postgresql://snetworkdba"
                           ":elcj2304@localhost/snetwork")
SQLALCHEMY_TRACK_MODIFICATIONS = False
