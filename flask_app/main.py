from dotenv import load_dotenv
import os

from flask import Flask, request
from flask import got_request_exception
from flask_restful import Resource, Api, abort
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, jwt_required
from flask_cors import CORS

from assessment_estimation.models.assessors.default_assessor import DefaultAssessor
from assessment_estimation.models.generators.assessment_generators import DefaultAssessmentGenerator
from assessment_estimation.services.assessment_service import AssessmentService, AssessmentNotFound, StudentNotFound
from assessment_estimation.storage.in_memory_storage.in_memory_storages import InMemoryStudentStorage, \
    InMemoryGroupStorage, InMemoryTaskStorage, InMemoryAssessmentStorage

JWT_SECRET_KEY_NAME = 'JWT_SECRET_KEY'
DEBUG_MODE_KEY_NAME = 'DEBUG_MODE'
THREADS_NUM_KEY = 'THREADS_NUM'


def log_exception(sender, exception, **extra):
    """ Log an exception to our logging framework """
    sender.logger.debug('Got exception during processing: %s', exception)


def prepare_and_config_api():
    load_dotenv()
    app = Flask(__name__)

    debug_mode = os.getenv(DEBUG_MODE_KEY_NAME, default='False').lower() == 'true'

    app.config[JWT_SECRET_KEY_NAME] = os.getenv(JWT_SECRET_KEY_NAME)
    jwt = JWTManager(app)
    CORS(app)

    errors = {
        'StudentNotFound': {
            'message': "A user with that username already exists.",
            'status': 404,
        },
        'AssessmentNotFound': {
            'message': "The assessment you are trying to use doesn't exists.",
            'status': 404,
        },
    }
    api = Api(app, errors=errors)

    got_request_exception.connect(log_exception, app)

    return app, api, debug_mode


def prepare_services():
    student_storage = InMemoryStudentStorage()
    group_storage = InMemoryGroupStorage()
    task_storage = InMemoryTaskStorage()
    waiting_assessment_storage = InMemoryAssessmentStorage()
    active_assessment_storage = InMemoryAssessmentStorage()
    done_assessment_storage = InMemoryAssessmentStorage()
    threads_num = int(os.getenv(THREADS_NUM_KEY, default=1))
    assessment_generator = DefaultAssessmentGenerator(threads_num, waiting_assessment_storage)
    assessor = DefaultAssessor()
    assessment_service = AssessmentService(student_storage, group_storage, task_storage, waiting_assessment_storage,
                                           active_assessment_storage, done_assessment_storage, assessment_generator,
                                           assessor)
    return assessment_service


class UserLogin(Resource):
    def post(self):
        json = request.get_json()
        if not json:
            return {'error': 'Username and password are required'}

        username = json.get('username')
        password = json.get('password')
        if username != 'admin' or password != 'habr':
            return {'error': 'Invalid username or password'}

        access_token = create_access_token(identity={
            'role': 'admin',
        }, expires_delta=False)
        result = {'token': access_token}
        return result


class Assessment(Resource):
    @jwt_required
    def get(self):
        """
        Get the assessment for the testee and admin
        :return:
        """
        return {'answer': 42}

    def post(self):
        """
        Create new assessment by admin
        :return:
        """
        pass

    def put(self):
        """
        End assessment by testee
        :return:
        """
        pass

    def patch(self):
        """
        Answer assessment by testee
        :return:
        """
        pass

    def delete(self):
        """
        Cancel assessment by admin
        :return:
        """
        pass


class Answer(Resource):
    def post(self):
        json = request.get_json()
        if not json:
            abort(400, message='No answer was sent')

        assessment_uuid = json.get('assessment_uid')
        if not assessment_uuid:
            abort(400, message='No assessment id provided')

        checked_answers = json.get('marked_answers')
        unchecked_answers = json.get('unmarked_answers')
        if not unchecked_answers and not checked_answers:
            abort(400, message='No answers provided')

        assessment_service.answer_assessment(assessment_uuid, checked_answers, unchecked_answers)
        return {'status': 'ok'}, 200


app, api, debug_mode = prepare_and_config_api()
assessment_service = prepare_services()
api.add_resource(UserLogin, '/api/login/')
api.add_resource(Assessment, '/api/assessment/')
api.add_resource(Answer, '/api/answer/')

if __name__ == '__main__':
    app.run(debug=debug_mode, host='0.0.0.0')
