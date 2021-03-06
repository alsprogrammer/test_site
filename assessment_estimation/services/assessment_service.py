import datetime
from typing import List, Callable, Set, Iterable
from assessment_estimation.storage.storages_abc import StudentStorage, TaskStorage, GroupStorage, AssessmentStorage
from assessment_estimation.models.models import Student, Assessment, Task


class StudentNotFound(KeyError):
    pass


class AssessmentNotFound(KeyError):
    pass


class AssessmentService:
    def __init__(self, student_storage: StudentStorage, group_storage: GroupStorage,
                 task_storage: TaskStorage, waiting_assessment_storage: AssessmentStorage,
                 active_assessment_storage: AssessmentStorage, done_assessment_storage: AssessmentStorage,
                 assessment_generator: Callable[[Student, List[Task], int, AssessmentStorage], None],
                 assessor: Callable[[Assessment], float]):
        self._student_storage = student_storage
        self._group_storage = group_storage
        self._task_storage = task_storage
        self._waiting_assessment_storage = waiting_assessment_storage
        self._active_assessment_storage = active_assessment_storage
        self._done_assessment_storage = done_assessment_storage
        self._assessment_generator = assessment_generator
        self._assessor = assessor

    def get_assessing_students(self) -> Set[Student]:
        return set([cur_assessment.student for cur_assessment in self._active_assessment_storage])

    def get_allowed_students(self) -> Set[Student]:
        return set([cur_assessment.student for cur_assessment in self._waiting_assessment_storage])

    def add_assessment(self, student_uid: str, topic_names: Iterable[str], task_num: int):
        if student_uid not in self._student_storage.keys():
            raise StudentNotFound()

        possible_tasks = [cur_task for cur_task in self._task_storage if cur_task.topics_task_is_on in topic_names]
        student = self._student_storage[student_uid]
        self._assessment_generator(student, possible_tasks, task_num, self._waiting_assessment_storage)

    def start_assessment(self, assessment_uid: str) -> Assessment:
        if assessment_uid not in self._waiting_assessment_storage.keys():
            raise AssessmentNotFound()

        assessment = self._waiting_assessment_storage[assessment_uid]
        assessment.started = datetime.datetime.now()
        self._active_assessment_storage[assessment.uuid] = assessment
        del self._waiting_assessment_storage[assessment_uid]

        return assessment

    def answer_assessment(self, assessment_uid: str, checked_option_uids: Iterable[str],
                          unchecked_option_uids: Iterable[str]) -> Assessment:
        if assessment_uid not in self._active_assessment_storage.keys():
            raise AssessmentNotFound()

        assessment = self._active_assessment_storage[assessment_uid]
        assessment.checked_uuids.append(checked_option_uids)
        for unchecked in unchecked_option_uids:
            assessment.checked_uuids.discard(unchecked)

    def remove_assessment(self, assessment_uid: str):
        if assessment_uid not in self._waiting_assessment_storage.keys():
            raise AssessmentNotFound()

        del self._waiting_assessment_storage[assessment_uid]

    def cancel_assessment(self, assessment_uid: str):
        if assessment_uid not in self._active_assessment_storage.keys():
            raise AssessmentNotFound()

        del self._active_assessment_storage[assessment_uid]

    def done_assessment(self, assessment_uid: str):
        if assessment_uid not in self._active_assessment_storage.keys():
            raise AssessmentNotFound()

        assessment = self._active_assessment_storage[assessment_uid]
        assessment.ended = datetime.datetime.now()
        self._assessor(assessment)
        self._done_assessment_storage[assessment_uid] = assessment
        del self._active_assessment_storage[assessment_uid]
