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

from app import views, models

# Loads the test set from the predefined file
test_set = models.TestSet(open(os.path.join(basedir, "test_set.xml")))

# Creates the dict for the student-test pairs
students_ready_to_test = {}
# Creates the dict for the student-test pairs that are in progress at the moment
testing_students = {}
