#!flask/bin/python
from app import app
from werkzeug.contrib.fixers import ProxyFix

from threading import Thread

from app import tasksets_condition, ready_to_test, q
from config import num_threads
import uuid

set_assessments = ready_to_test


def handle_assessment(q):

    global set_assessments
    assessment_dict = q.get()
    assessment = assessment_dict['taskset'].create_test(assessment_dict['taskset'].tasks_num,
                                                        student=assessment_dict['student'])
    tasksets_condition.acquire()
    set_assessments.update({uuid.uuid4().hex: assessment})
    tasksets_condition.release()


app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
    for i in range(num_threads):
        worker = Thread(target=handle_assessment, args=(q,))
        worker.setDaemon(True)
        worker.start()

    app.run(debug=True)

    q.join()