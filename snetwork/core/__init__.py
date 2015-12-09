from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_oauthlib.provider import OAuth2Provider
from flask_cache import Cache
from flask_bcrypt import Bcrypt

app = Flask('snetwork')
app.config.from_envvar('SNETWORK_CONFIG')
app.db = db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
oauth = OAuth2Provider(app)
cache = Cache(app)
bcrypt = Bcrypt(app)
