from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask('snetwork')
app.config.from_envvar('SNETWORK_CONFIG')
app.db = db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
