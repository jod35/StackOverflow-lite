from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import DevConfig
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager

app=Flask(__name__)
app.config.from_object(DevConfig)


db=SQLAlchemy(app)
migrate=Migrate(app,db)
bcrypt=Bcrypt(app)
login_manager=LoginManager()
login_manager.init_app(app)


from . import views