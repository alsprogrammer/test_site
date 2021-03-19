from typing import Iterable, Optional, Dict, Set, Union, List

from abc import ABC
import uuid
import datetime

from pydantic.main import BaseModel


class Model(BaseModel, ABC):
    uuid: str = uuid.uuid4().hex

    def __init__(self):
        super(Model, self).__init__()


class Student(Model):
    """The student class. Describes the student's name and group"""
    first_name: str
    sur_name: str
    last_name: str
    group_uuid: str
    group_name: str

    def __init__(self, last_name: str = "", first_name: str = "", sur_name: str = "", group: 'Group' = None):
        """Create a new student.

        Keyword arguments:
        last_name - last name of the student
        first_name - first name of the student
        sur_name - surname of the student (default is blank line)
        group - group the student blongs to (default is None)
        """
        super().__init__()
        self.first_name = first_name
        self.sur_name = sur_name
        self.last_name = last_name
        self.group_uuid = group.uuid
        self.group_name = group.name

    def __repr__(self):
        return "{lname} {fname} ({gname})".format(lname=self.last_name, fname=self.first_name, gname=self.group_name)


class Group(Model):
    """The group class. Describes the group and its students"""
    speciality: str
    start_year: int
    name: str
    students: Dict[str, str] = {}  # student id -> student full name

    def __init__(self, speciality, year, name):
        """Create a new group.

        Keyword arguments:
        speciality - the name of the speciality the group belongs to
        year - the year the group was formed
        name - the name of the group
        """
        super().__init__()
        self.speciality = speciality
        self.start_year = year
        self.name = name

    def __repr__(self):
        return "{name} ({year}, {spec})".format(name=self.name, year=self.start_year, spec=self.speciality)


class Task(Model):
    """Describes single task in an assessment"""
    topics_task_is_on: List[str] = []
    stem: Union[str, 'TaskOption']
    answers: Set['TaskOption'] = set()
    distractors: Set['TaskOption'] = set()

    def __init__(self, stem: Union[str, 'TaskOption'], topics: Union[str, Iterable[str]]):
        assert stem is not None, "Stem has to be provided"
        assert topics is not None, "The topics the task is on have to be provided"

        super().__init__()

        self.topics_task_is_on = list(topics) if isinstance(topics, Iterable) else [topics]
        self.stem = stem

    def add_answer(self, answer: Union[str, 'TaskOption']):
        """
        Add answer to the task
        :param answer: TaskOption, answer to add
        :return: None
        """
        if isinstance(answer, str) or isinstance(answer, TaskOption):
            self.answers.add(answer)
        else:
            raise TypeError()

    def add_distractor(self, distractor: Union[str, 'TaskOption']):
        """
        Add distractor to the task
        :param distractor: TaskOption, distractor to add
        :return: None
        """
        if isinstance(distractor, str) or isinstance(distractor, TaskOption):
            self.distractors.add(distractor)
        else:
            raise TypeError()

    def __repr__(self):
        return "{}".format(self.stem)


class TaskOption(Model):
    """Single task element - a stem, an answer, or a distractor"""
    text: str
    picture: Optional[str]  # a base64-encoded png picture

    def __init__(self, text: str = "", picture: str = None):
        super().__init__()
        self.text = text
        self.picture = picture

    def __repr__(self):
        return "{}".format(self.text)


class Assessment(Model):
    """The assessment for the student"""
    created: datetime = datetime.datetime.now()
    started: Optional[datetime] = None
    ended: Optional[datetime] = None
    time_limit: int
    name: str = ""
    answer_times: List[int] = []
    student_uuid: str  # the student to be tested
    student_name: str
    answers_uuids: Set[str] = set()  # a list of answers UUIDs
    distractors_uuids: Set[str] = set()  # a list of distractors UUIDs
    tasks_uuids: List[str] = []  # a list of all task uuids
    threshold: int = 50
    checked_uuids: List[str] = set()
    mistaken_uuids: List[str] = set()
    mistaken_tasks: List[str] = set()
    score: float = 0
    real_score: float = 0

    def __init__(self, student: Student, name: str):
        """
        Create a new assessment from the given student
        :param student: a student to create the assessment for
        """
        assert name is not None and name != "", "The name of the test has to be provided"
        super().__init__()
        self.name = name
        self.student_uuid = student.uuid
        self.student_name = str(student)


class TopicSet(Set, Model):
    def __init__(self, topics_to_add: Optional[Iterable[str]] = None):
        super().__init__()
        if topics_to_add:
            for current_topic in topics_to_add:
                self.add(current_topic)
        else:
            self.clear()
