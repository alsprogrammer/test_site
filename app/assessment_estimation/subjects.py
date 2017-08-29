from bs4 import BeautifulSoup
from abc import ABCMeta, abstractmethod
import copy
import uuid
import random


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

    def __init__(self, stem, theme=None, picture=None):
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

    def __init__(self, text, picture=None):
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
        self.tasks = []

    def __init__(self, tasks_list):
        self.tasks = copy.copy(tasks_list)

    def __init__(self, assessment_desciption):
        self.tasks = []
        xml_file = open(assessment_desciption)
        text = xml_file.readlines()
        xml_file.close()

        for task in BeautifulSoup(" ".join(text), "xml").findAll("Question"):
            image = task.find("Image")
            image_text = image.contents[0] if image else None
            stem = task.find("Text").contents[0]
            new_task = Task(task.contents[1].text, theme=task["theme"], picture=image_text)
            options = task.findAll("Variant")
            for option in options:
                opt_text = option.find("Text").contents
                opt_image = option.find("Image")
                opt_image_text = image.contents[0] if opt_image else None
                if option["right"] == "+":
                    new_answer = TaskOption(opt_text, picture=opt_image_text)
                    new_task.add_answer(new_answer)
                else:
                    new_distractor = TaskOption(opt_text, picture=opt_image_text)
                    new_task.add_distractor(new_distractor)

            self.tasks.append(new_task)

    def create_test(self, tasks_num):
        if tasks_num <= 0:
            raise ValueError("Wrong number of the tasks in the assessment: the number of tasks can't be zero or negative")

        if tasks_num > len(self.tasks):
            raise ValueError("Wrong number of the tasks in the assessment: greater than tasks in task pool")

        new_assessment = Assessment()
        tasks = random.sample(self.tasks, tasks_num)
        random.shuffle(tasks)

        for cur_task in tasks:
            options = []

            for cur_answer in cur_task.answers:
                cur_uuid = uuid.uuid4().hex
                options.append({"text": cur_answer.text, "picture": cur_answer.picture, "uuid": cur_uuid})
                new_assessment.answers_uuids.append(cur_uuid)

            for cur_distractor in cur_task.answers:
                cur_uuid = uuid.uuid4().hex
                options.append({"text": cur_distractor.text, "picture": cur_distractor.picture, "uuid": cur_uuid})
                new_assessment.distractors_uuids.append(cur_uuid)

        new_assessment.tasks.append(cur_task)

        return new_assessment

    def to_dict(self):
        pass

    def from_dict(self):
        pass


class Assessment(FromToDict):
    """The assessment for the student"""
    def __init__(self):
        self.answers_uuids = [] # a list of answers UUIDs
        self.distractors_uuids = [] # a list of distractors UUIDs
        self.tasks = [] # a list of dicts each contains stem and a list of options (not answers/distractors)

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
