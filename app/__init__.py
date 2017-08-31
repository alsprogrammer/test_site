import os
from flask import Flask
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir
from pathlib import Path
import uuid
from assessment_estimation.subjects import Group
import json


app = Flask(__name__)
app.config.from_object('config')

lm = LoginManager()
lm.init_app(app)
oid = OpenID(app, os.path.join(basedir, 'tmp'))

groups_to_test = {}  # groups to test
students_ready_to_test = {}  #
passing = {}  # the dict of the assessments that are passing at the moment
passed = {}  # the dict of the passed assessments

from app import views, models

folder = Path(app.config['DATA_PATH'])
files_with_maps = folder.glob('*.gjsn')

for file in files_with_maps:
    group_file = open(file, encoding='utf-8')
    group_text = group_file.read()
    group_file.close()
    group_json = json.loads(group_text)

    new_group = Group()
    new_group.from_dict(group_json)
    groups_to_test.update({"uuid": uuid.uuid4().hex, "group": new_group})
