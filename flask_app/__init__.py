import os
from flask import Flask
from flask_login import LoginManager
from flask_openid import OpenID

from assessment_estimation.models.assessors import DefaultAssessor
from config import basedir
from pathlib import Path
import json

from assessment_estimation.storage.in_memory_storage.in_memory_storages import InMemoryStudentStorage
from assessment_estimation.storage.in_memory_storage.in_memory_storages import InMemoryAssessmentStorage
from assessment_estimation.storage.in_memory_storage.in_memory_storages import InMemoryGroupStorage
from assessment_estimation.storage.in_memory_storage.in_memory_storages import InMemoryTaskStorage
from assessment_estimation.services.assessment_service import AssessmentService
from assessment_estimation.models.generators.assessment_generators import DefaultAssessmentGenerator

app = Flask(__name__)
app.config.from_object('config')

lm = LoginManager()
lm.init_app(app)
oid = OpenID(app, os.path.join(basedir, 'tmp'))

students_to_test = InMemoryStudentStorage()
groups_to_test = InMemoryGroupStorage()
ready_to_test = InMemoryAssessmentStorage()
tasks = InMemoryTaskStorage()
passing = InMemoryAssessmentStorage()
passed = InMemoryAssessmentStorage()

assessment_generator = DefaultAssessmentGenerator(4, ready_to_test)

assessment_service = AssessmentService(students_to_test, groups_to_test, tasks, ready_to_test, passing,
                                       passed, assessment_generator, DefaultAssessor())

from flask_app import views

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
#test_files = folder.glob('*.tjsn')
#for cur_file in test_files:
#    test_file = open(os.path.join(app.config["DATA_PATH"], cur_file.name), mode="r", encoding='utf-8')
#    test_xml = test_file.read()
#    test_file.close()
#    test_json = json.loads(test_xml)
#
#    new_test = TasksPool()
#    new_test.from_dict(test_json)
#    tasksets.update({cur_file.name[:-5]: new_test})
