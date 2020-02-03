from typing import Iterable, Optional

from bs4 import BeautifulSoup, Tag
from abc import ABCMeta, ABC, abstractmethod
import copy
import uuid
import random
import datetime
from assessment_estimation.func_libs import assesst
import numpy as np


class Model(ABC):
    def __init__(self):
        self.uuid = uuid.uuid4().hex


class Group(Model):
    """The group class. Describes the group and its students"""

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
        self.students = {}

    def __repr__(self):
        return "{name} ({year}, {spec})".format(name=self.name, year=self.start_year, spec=self.speciality)


class Student(Model):
    """The student class. Describes the student's name and group"""

    def __init__(self, last_name: str = "", first_name: str = "", sur_name:str = "", group: Group = None):
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
        self.group = group

    def __repr__(self):
        return "{lname} {fname} ({gname})".format(lname=self.last_name, fname=self.first_name, gname=self.group.name)


class Task(Model):
    """Describes single task in an assessment"""
    def __init__(self, stem="", theme=None, picture=None):
        super().__init__()
        self.theme = theme
        self.stem = stem
        self.picture = picture
        self.answers = set()
        self.distractors = set()

    def add_answer(self, answer):
        """
        Add answer to the task
        :param answer: TaskOption, answer to add
        :return: None
        """
        if isinstance(answer, str) or isinstance(answer, TaskOption):
            self.answers.add(answer)
        else:
            raise TypeError()

    def add_distractor(self, distractor):
        """
        Add distractor to the task
        :param distractor: TaskOption, distractor to add
        :return: None
        """
        if isinstance(distractor, str) or isinstance(distractor, TaskOption):
            self.distractors.add(distractor)
        else:
            raise TypeError()

    def get_html_picture(self):
        return "data:image/png;base64, {picture_code}".format(picture_code=self.picture)

    def __repr__(self):
        return "{}".format(self.stem)


class TaskOption(Model):
    """Single task element - answer or distractor"""
    def __init__(self, text="", picture=None):
        super().__init__()
        self.text = text
        self.picture = picture

    def get_html_picture(self):
        return "data:image/png;base64, {picture_code}".format(picture_code=self.picture)

    def __repr__(self):
        return "{}".format(self.text)


class Assessment(Model):
    """The assessment for the student"""
    def __init__(self, student=None):
        """
        Create a new assessment fro the given student
        :param student: a student to create the assessment for
        """
        super().__init__()
        self.created = datetime.datetime.now()
        self.started = None
        self.ended = None
        self.time_limit = 0
        self.name = ""
        self.answer_times = []
        self.student = student  # the student to be tested
        self.answers_uuids = set()  # a list of answers UUIDs
        self.distractors_uuids = set()  # a list of distractors UUIDs
        self.tasks = []  # a list of dicts each contains stem and a list of options (not answers/distractors)
        self.threshold = 50
        self.checked_uuids = set()
        self.mistaken_uuids = set()
        self.mistaken_tasks = set()
        self.score = 0
        self.real_score = 0
        self.uuid = uuid.uuid4().hex


class TopicSet(Model):
    def __init__(self, topics_iterable: Optional[Iterable[str]] = None) -> None:
        super().__init__()
        if topics_iterable:
            self._topics_set = set(topics_iterable)
        else:
            self._topics_set = set()

    def get_topics(self) -> Iterable[str]:
        return set(self._topics_set)

    def add_topic(self, topic: str) -> None:
        if topic:
            self._topics_set.add(topic)

    def remove_topic(self, topic: str) -> None:
        if topic:
            self._topics_set.remove(topic)
