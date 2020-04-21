from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from suggest_tool.paths import *
import os.path
if not os.path.exists(USERS_PATH):

	from suggest_tool.models import User
	save_pck([User()], USERS_PATH)

import signal
import sys

def signal_handler(signal, frame):
	if load_pck(UPDATE_PATH) == 1:
		save_pck(0, UPDATE_PATH)
	sys.exit(0)	

signal.signal(signal.SIGINT, signal_handler)

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from suggest_app import routes, models
