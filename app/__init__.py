from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
import flask_excel as excel
from flask_migrate import Migrate
from config import Config
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
admin = Admin(app)
excel.init_excel(app)
mail = Mail(app)

from app import routes, models
