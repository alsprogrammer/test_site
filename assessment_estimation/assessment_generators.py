from typing import Callable, List
from queue import Queue
import threading
from random import shuffle

from assessment_estimation.subjects import Task, Assessment


class StandardGenerator:
    def __init__(self, threads_num: int, assessment_handler: Callable[[Queue], None]):
        creating_assessments_queue = Queue(maxsize=0)

        for i in range(threads_num):
            worker = threading.Thread(target=assessment_handler, args=(creating_assessments_queue,))
            worker.setDaemon(True)
            worker.start()

    def __call__(self, tasks: List[Task], task_num: int) -> Assessment:
        if len(tasks) < task_num:
            raise

        new_assessment = Assessment()
        new_assessment.tasks = StandardGenerator._select_tasks(tasks, task_num)
        StandardGenerator._build_options(new_assessment)

        return new_assessment

    @staticmethod
    def _select_tasks(tasks: List[Task], task_num: int) -> List[Task]:
        shuffled_task_list = tasks.copy()
        shuffle(shuffled_task_list)
        return shuffled_task_list[:task_num]

    @staticmethod
    def _build_options(assessment: Assessment):
        for cur_task in assessment.tasks:
            assessment.answers_uuids.update([cur_answer.uuid for cur_answer in cur_task.answers])
            assessment.distractors_uuids.update([cur_distractor.uuid for cur_distractor in cur_task.distractors])
