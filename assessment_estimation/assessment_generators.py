from typing import Callable, List
from queue import Queue
import threading

from assessment_estimation.subjects import Task, Assessment


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


class StandardGenerator:
    def __init__(self, threads_num: int, assessment_handler: Callable[[Queue], None]):
        creating_assessments_queue = Queue(maxsize=0)
        tasksets_condition = threading.Condition()

        for i in range(threads_num):
            worker = threading.Thread(target=assessment_handler, args=(creating_assessments_queue,))
            worker.setDaemon(True)
            worker.start()

    def __call__(self, tasks: List[Task], task_num: int) -> Assessment:
        pass
