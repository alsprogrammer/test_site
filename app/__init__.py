import os
from flask import Flask
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir
from pathlib import Path
from assessment_estimation.subjects import Group
import json

from queue import Queue
import threading

app = Flask(__name__)
app.config.from_object('config')

lm = LoginManager()
lm.init_app(app)
oid = OpenID(app, os.path.join(basedir, 'tmp'))

groups_to_test = {}  # groups to test at the moment
ready_to_test = {}  # the not started yet assessments (but given for the students)
tasksets = {}  # the test ready to be used to generate assessments
passing = {}  # the dict of the assessments that are passing at the moment
passed = {}  # the dict of the passed assessments

creating_assessments_queue = Queue(maxsize=0)
tasksets_condition = threading.Condition()

from app import views
from assessment_estimation.subjects import *

folder = Path(app.config['DATA_PATH'])

# loading groups
files_with_maps = folder.glob('*.gjsn')
for cur_file in files_with_maps:
    group_file = open(os.path.join(app.config["DATA_PATH"], cur_file.name), mode="r", encoding='utf-8')
    group_text = group_file.read()
    group_file.close()
    group_json = json.loads(group_text)

    new_group = Group(group_json["spec"], group_json["year"], group_json["name"])
    new_group.from_dict(group_json)
    groups_to_test.update({cur_file.name[:-5]: new_group})

# loading tests
test_files = folder.glob('*.tjsn')
for cur_file in test_files:
    test_file = open(os.path.join(app.config["DATA_PATH"], cur_file.name), mode="r", encoding='utf-8')
    test_xml = test_file.read()
    test_file.close()
    test_json = json.loads(test_xml)

    new_test = TasksPool()
    new_test.from_dict(test_json)
    tasksets.update({cur_file.name[:-5]: new_test})
