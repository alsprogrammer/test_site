import os
from flask import Flask
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir
from bs4 import BeautifulSoup


app = Flask(__name__)
app.config.from_object('config')

lm = LoginManager()
lm.init_app(app)
oid = OpenID(app, os.path.join(basedir, 'tmp'))

test_set = BeautifulSoup(open(os.path.join(basedir, "test_set.xml")), "lxml")

from app import views, models
