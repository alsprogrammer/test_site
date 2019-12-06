from typing import Iterable, Optional

from abc import ABCMeta, ABC, abstractmethod
import uuid
import datetime
from assessment_estimation.func_libs import assesst


class FromToDict:
    __metaclass__ = ABCMeta

    @abstractmethod
    def to_dict(self):
        """
        Get a json description of the object, all subclasses are represented by its string representations
        :return: json object
        """

    @abstractmethod
    def from_dict(self, descr):
        """
        Load an object from its json desciprtion
        :return: None
        """


class Model(ABC):
    def __init__(self):
        self.uuid = uuid.uuid4().hex


class Student(Model, FromToDict):
    """The student class. Describes the student's name and group"""

    def __init__(self, last_name="", first_name="", sur_name="", group=None):
        """Create a new student.

        Keyword arguments:
        last_name - last name of the student
        first_name - first name of the student
        sur_name - surname of the student (default is blank line)
        group - group the student blongs to (default is None)
        """
        self.first_name = first_name
        self.sur_name = sur_name
        self.last_name = last_name
        self.group = group

    def from_dict(self, descr):
        self.last_name = descr["last_name"]
        self.first_name = descr["first_name"]
        self.sur_name = descr["surname"]
        self.group = descr["group_name"]

    def to_dict(self):
        return {"last_name": self.last_name, "first_name": self.first_name, "surname": self.sur_name,
                "group_name": self.group.name}

    def __repr__(self):
        return "{lname} {fname} ({gname})".format(lname=self.last_name, fname=self.first_name, gname=self.group.name)


class Group(Model, FromToDict):
    """The group class. Describes the group and its students"""

    def __init__(self, speciality, year, name):
        """Create a new group.

        Keyword arguments:
        speciality - the name of the speciality the group belongs to
        year - the year the group was formed
        name - the name of the group
        """
        self.speciality = speciality
        self.start_year = year
        self.name = name
        self.students = {}

    def add_student(self, student):
        """Add a new student.
        Changes the group property of the student object.

        student - the student to be added to the group
        """
        self.students.update({student.uuid: student})
        student.group = self

    def from_dict(self, descr):
        self.speciality = descr["spec"]
        self.start_year = descr["year"]
        self.name = descr["name"]
        students = {cur_stud_uid: Student(descr["students"][cur_stud_uid]["last_name"],
                                          first_name=descr["students"][cur_stud_uid]["first_name"],
                                          sur_name=descr["students"][cur_stud_uid]["surname"],
                                          group=self) for cur_stud_uid in descr["students"]}
        self.students = students

    def to_dict(self):
        students = {cur_stud_uid:self.students[cur_stud_uid].to_dict() for cur_stud_uid in self.students}
        return {"name": self.name, "spec": self.speciality, "year": self.start_year, "students": students}

    def __repr__(self):
        return "{name} ({year}, {spec})".format(name=self.name, year=self.start_year, spec=self.speciality)


class Task(Model, FromToDict):
    """Describes single task in an assessment"""
    def __init__(self, stem="", theme=None, picture=None):
        self.theme = theme
        self.stem = stem
        self.picture = picture
        self.answers = []
        self.distractors = []

    def add_answer(self, answer):
        """
        Add answer to the task
        :param answer: TaskOption, answer to add
        :return: None
        """
        if isinstance(answer, str) or isinstance(answer, TaskOption):
            self.answers.append(answer)
        else:
            raise TypeError()

    def add_distractor(self, distractor):
        """
        Add distractor to the task
        :param distractor: TaskOption, distractor to add
        :return: None
        """
        if isinstance(distractor, str) or isinstance(distractor, TaskOption):
            self.distractors.append(distractor)
        else:
            raise TypeError()

    def get_html_picture(self):
        return "data:image/png;base64, {picture_code}".format(picture_code=self.picture)

    def from_dict(self, descr):
        self.theme = descr['theme']
        self.stem = descr['stem']
        self.picture = descr['picture']
        self.answers = []
        for cur_option in descr['answers']:
            new_option = TaskOption()
            new_option.from_dict(cur_option)
            self.answers.append(new_option)
        self.distractors = []
        for cur_option in descr['distractors']:
            new_option = TaskOption()
            new_option.from_dict(cur_option)
            self.distractors.append(new_option)

    def to_dict(self):
        answers = [cur_option.to_dict() for cur_option in self.answers]
        distractors = [cur_option.to_dict() for cur_option in self.distractors]

        return {'theme': self.theme, 'stem': self.stem, 'picture': self.picture, 'answers': answers, 'distractors': distractors}

    def __repr__(self):
        return "{}".format(self.stem)


class TaskOption(Model, FromToDict):
    """Single task element - answer or distractor"""
    def __init__(self, text="", picture=None):
        self.text = text
        self.picture = picture

    def from_dict(self, descr):
        self.text = descr['text']
        self.picture = descr['picture']

    def get_html_picture(self):
        return "data:image/png;base64, {picture_code}".format(picture_code=self.picture)

    def to_dict(self):
        return {'text': self.text, 'picture': self.picture}

    def __repr__(self):
        return "{}".format(self.text)


class Assessment(Model, FromToDict):
    """The assessment for the student"""
    def __init__(self, student=None):
        """
        Create a new assessment fro the given student
        :param student: a student to create the assessment for
        """
        self.created = datetime.datetime.now()
        self.started = None
        self.ended = None
        self.time_limit = 0
        self.name = ""
        self.answer_times = []
        self.student = student  # the student to be tested
        self.answers_uuids = set([])  # a list of answers UUIDs
        self.distractors_uuids = set([])  # a list of distractors UUIDs
        self.tasks = []  # a list of dicts each contains stem and a list of options (not answers/distractors)
        self.threshold = 50
        self.checked_uuids = set([])
        self.mistaken_uuids = set([])
        self.mistaken_tasks = set([])
        self.score = 0
        self.real_score = 0
        self.uuid = uuid.uuid4().hex

    def from_dict(self, descr):
        pass

    def to_dict(self):
        dict_to_export = {}
        dict_to_export.update({'created': self.created.strftime("%Y-%m-%d %H:%M:%S"),
                               'started': self.started.strftime("%Y-%m-%d %H:%M:%S"),
                               'ended': self.ended.strftime("%Y-%m-%d %H:%M:%S"),
                               'student': self.student.to_dict(), 'score': self.score, 'real_score': self.real_score,
                               'answers': list(self.answers_uuids), 'distractors': list(self.distractors_uuids),
                               'tasks': self.tasks, 'threshold': self.threshold,
                               'checked': list(self.checked_uuids), 'mistaken': list(self.mistaken_uuids)})
        return dict_to_export


class TopicSet(Model):
    def __init__(self, topics_iterable: Optional[Iterable[str]]=None) -> None:
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
