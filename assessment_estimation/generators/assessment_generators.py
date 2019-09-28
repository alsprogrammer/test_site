from abc import ABC, abstractmethod
from typing import List
from queue import Queue
import threading
from random import shuffle

from assessment_estimation.storage.storages_abc import AssessmentStorage
from assessment_estimation.models.models import Task, Assessment, Student


class AssessmentGenerator(ABC):
    @abstractmethod
    def __call__(self, student: Student, tasks: List[Task], task_num: int, assessment_storage: AssessmentStorage):
        pass


class DefaultAssessmentGenerator(AssessmentGenerator):
    def __init__(self, threads_num: int, assessment_storage: AssessmentStorage):
        self._calculate_assessment_threshold_queue = Queue(maxsize=0)

        for i in range(threads_num):
            worker = threading.Thread(target=DefaultAssessmentGenerator._calculate_threshold,
                                      args=(self._calculate_assessment_threshold_queue, assessment_storage))
            worker.setDaemon(True)
            worker.start()

    def __call__(self, student: Student, tasks: List[Task], task_num: int, assessment_storage: AssessmentStorage):
        if len(tasks) < task_num:
            raise ValueError('The number of the tasks in the assessement you want is higher the the number of the available tasks.')

        new_assessment = Assessment()
        new_assessment.tasks = DefaultAssessmentGenerator._select_tasks(tasks, task_num)
        DefaultAssessmentGenerator._set_answers_distractors(new_assessment)
        self._calculate_assessment_threshold_queue.put(new_assessment)

    def close(self):
        self._calculate_assessment_threshold_queue.join()

    @staticmethod
    def _select_tasks(tasks: List[Task], task_num: int) -> List[Task]:
        shuffled_task_list = tasks.copy()
        shuffle(shuffled_task_list)
        return shuffled_task_list[:task_num]

    @staticmethod
    def _set_answers_distractors(assessment: Assessment):
        for cur_task in assessment.tasks:
            assessment.answers_uuids.update([cur_answer.uuid for cur_answer in cur_task.answers])
            assessment.distractors_uuids.update([cur_distractor.uuid for cur_distractor in cur_task.distractors])

    @staticmethod
    def _calculate_threshold(assessment_queue: Queue, assessment_storage: AssessmentStorage):
        while True:
            assessment = assessment_queue.get()
            assessment.threshold = 60
            assessment_storage[assessment.uuid] = assessment
            assessment_queue.task_done()
