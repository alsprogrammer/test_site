from bs4 import BeautifulSoup, Tag
from abc import ABCMeta, abstractmethod
import copy
import uuid
import random
import datetime
from .func_libs import assesst
import numpy as np


class FromToDict():
    __metaclass__ = ABCMeta

    @abstractmethod
    def to_dict(self):
        """
        Get a json description of the object, all subclasses are represented by its string representations
        :return: json object
        """

    @abstractmethod
    def from_dict(self):
        """
        Load an object from its json desciprtion
        :return: None
        """


class Student(FromToDict):
    """The student class. Describes the student's name and group"""

    def __init__(self):
        """Create new student with no name and group"""
        self.first_name = ""
        self.sur_name = ""
        self.last_name = ""
        self.group = None

    def __init__(self, last_name, first_name="", sur_name="", group=None):
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

    def __repr__(self):
        return "{lname} {fname} ({gname})".format(lname=self.last_name, fname=self.last_name, gname=self.group)


class Group:
    """The group class. Describes the group and its students"""

    def __init__(self):
        # type: () -> object
        """Create new group with no name, speciality, start year and the empty list of the students"""
        self.speciality = ""
        self.start_year = -1;
        self.name = ""
        self.students = []

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
        self.students = []

    def add_student(self, student):
        """Add a new student.
        Changes the group property of the student object.

        student - the student to be added to the group
        """
        self.students.append(student)
        student.group = self

    def __repr__(self):
        return "{name} ({year}, {spec})".format(name=self.name, year=self.start_year, spec=self.speciality)


class Task(FromToDict):
    """Describes single task in an assessment"""
    def __init__(self):
        self.theme = ""
        self.stem = ""
        self.picture = None
        self.answers = []
        self.distractors = []

    def __init__(self, stem="", theme=None, picture=None):
        self.theme = theme
        self.stem = stem
        self.picture = picture
        self.answers = []
        self.distractors = []

    def add_answer(self, answer):
        """
        Add answer tp the task
        :param answer: answer to add
        :return: None
        """
        if isinstance(answer, str) or isinstance(answer, TaskOption):
            self.answers.append(answer)
        else:
            raise TypeError()

    def add_distractor(self, distractor):
        """
        Add answer tp the task
        :param distractor: answer to add
        :return: None
        """
        if isinstance(distractor, str) or isinstance(distractor, TaskOption):
            self.distractors.append(distractor)
        else:
            raise TypeError()

    def from_dict(self):
        pass

    def to_dict(self):
        pass

    def __repr__(self):
        return "{}".format(self.stem)


class TaskOption(FromToDict):
    """Single task element - answer or distractor"""
    def __init__(self):
        self.text = ""
        self.picture = None

    def __init__(self, text="", picture=None):
        self.text = text
        self.picture = picture

    def from_dict(self):
        pass

    def to_dict(self):
        pass

    def __repr__(self):
        return "{}".format(self.text)


class TasksPool(FromToDict):
    """A set of tasks to choose the tasks for a particular assessment from"""

    def __init__(self):
        self.threshold = 0.05
        self.tasks = []

    def __init__(self, tasks_list):
        self.threshold = 0.05
        self.tasks = copy.copy(tasks_list)

    def __init__(self, assessment_desciption):
        self.threshold = 0.05
        self.tasks = []
        xml_file = open(assessment_desciption)
        text = xml_file.readlines()
        xml_file.close()

        for task in BeautifulSoup(" ".join(text), "xml").findAll("Question"):
            new_task = Task()
            new_task.theme = task.attrs["theme"]
            for child in task.children:
                if isinstance(child, Tag):
                    if child.name == "Text":
                        new_task.stem = child.text
                    elif child.name == "Image":
                        new_task.picture = child.text
                    elif child.name == "Variant":
                        new_option = TaskOption()
                        for element in child.children:
                            if isinstance(element, Tag):
                                if element.name == "Text":
                                    new_option.text = element.text
                                elif element.name == "Image":
                                    new_option.picture = element.text

                        if child.attrs["right"] == "+":
                            new_task.answers.append(new_option)
                        else:
                            new_task.distractors.append(new_option)

            self.tasks.append(new_task)

    def create_test(self, tasks_num, student):
        if tasks_num <= 0:
            raise ValueError("Wrong number of the tasks in the assessment: the number of tasks can't be zero or negative")

        if tasks_num > len(self.tasks):
            raise ValueError("Wrong number of the tasks in the assessment: greater than tasks in task pool")

        new_assessment = Assessment()
        tasks = random.sample(self.tasks, tasks_num)
        random.shuffle(tasks)

        descr = []
        for cur_task in tasks:
            options = []

            for cur_answer in cur_task.answers:
                cur_uuid = uuid.uuid4().hex
                options.append({"text": cur_answer.text, "picture": cur_answer.picture, "uuid": cur_uuid})
                new_assessment.answers_uuids.add(cur_uuid)

            for cur_distractor in cur_task.distractors:
                cur_uuid = uuid.uuid4().hex
                options.append({"text": cur_distractor.text, "picture": cur_distractor.picture, "uuid": cur_uuid})
                new_assessment.distractors_uuids.add(cur_uuid)

            random.shuffle(options)
            new_task = {"stem": cur_task.stem, "picture": cur_task.picture, "theme": cur_task.theme, "options": options}
            new_assessment.tasks.append(new_task)

            descr.append({'answers_num': len(cur_task.answers), 'distractors_num': len(cur_task.distractors)})

        assessments_num = 10000

        assessments = []
        for i in range(assessments_num):
            assessments.append(assesst(items_num=len(tasks), assesst_props=descr, choice=True))

        values = np.unique(assessments)
        values1 = np.append(values, [1.1])

        hist, bins = np.histogram(assessments, bins=values1)

        hist_sum = np.sum(hist)

        hist = list(hist / float(hist_sum))

        sum = 0
        index = 0
        hist.reverse()
        for i, elem in enumerate(hist):
            sum += elem
            if sum > self.threshold:
                index = i
                break
        new_assessment.threshold = values[-(index + 1)] * 100

        return new_assessment

    def to_dict(self):
        pass

    def from_dict(self):
        pass


class Assessment(FromToDict):
    """The assessment for the student"""
    def __init__(self, student=None):
        self.created = datetime.datetime.now()
        self.started = None
        self.ended = None
        self.answer_times = []
        self.student = student  # the student to be tested
        self.answers_uuids = set([])  # a list of answers UUIDs
        self.distractors_uuids = set([])  # a list of distractors UUIDs
        self.tasks = []  # a list of dicts each contains stem and a list of options (not answers/distractors)
        self.threshold = 50

    def get_score(self, answers):
        if not isinstance(answers, set):
            raise ValueError("The answers should be the set of uuids.")

        all_options = self.answers_uuids.union(self.distractors_uuids)
        not_checked = all_options.difference(answers)

        score = float(len(self.answers_uuids & answers) + len(self.distractors_uuids & not_checked)) / float(len(all_options)) * 100.0
        real_score = (score - self.threshold) / (100 - self.threshold) * 100.0

        return real_score if real_score > 0 else 0, self.threshold, score

    def from_dict(self):
        pass

    def to_dict(self):
        pass


class TestingStudent:
    """A student-test combination being tested.
    Contains a beautifulsoup xml description of the test and the student object.
    """

    def __init__(self):
        """Create a new empty student-test combination."""
        self.test_bs = None
        self.student = None

    def __init__(self, student, test_bs):
        """Create a new empty student-test combination.

        Keyword arguments:
        student - a new-joined student.
        test_bs - beautyfulsoup description of the test
        """
        self.test_bs = test_bs
        self.student = student
