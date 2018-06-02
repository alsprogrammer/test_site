#!flask/bin/python
from app import app
from werkzeug.contrib.fixers import ProxyFix

from threading import Thread

from app import tasksets_condition, ready_to_test, creating_assessments_queue
from config import num_threads
import uuid

set_assessments = ready_to_test


def handle_assessment(q):

    global set_assessments

    while True:
        assessment_dict = q.get()

        assessment = assessment_dict['taskset'].create_test(assessment_dict['taskset'].tasks_num,
                                                        student=assessment_dict['student'])
        tasksets_condition.acquire()
        set_assessments.update({uuid.uuid4().hex: assessment})
        tasksets_condition.release()

        q.task_done()


app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
    for i in range(num_threads):
        worker = Thread(target=handle_assessment, args=(creating_assessments_queue,))
        worker.setDaemon(True)
        worker.start()

    app.run(debug=True)

    creating_assessments_queue.join()