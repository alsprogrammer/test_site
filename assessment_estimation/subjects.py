from bs4 import BeautifulSoup, Tag
from abc import ABCMeta, abstractmethod
import copy
import uuid
import random
import datetime
from .func_libs import assesst
import numpy as np


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


class Student(FromToDict):
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


class Group(FromToDict):
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
        self.students.update({uuid.uuid4().hex: student})
        student.group = self

    def from_dict(self, descr):
        self.speciality = descr["spec"]
        self.start_year = descr["year"]
        self.name = descr["name"]
        students = {cur_stud_uid: Student(descr["students"][cur_stud_uid]["last_name"], first_name=descr["students"][cur_stud_uid]["first_name"], sur_name=descr["students"][cur_stud_uid]["surname"],
                            group=self) for cur_stud_uid in descr["students"]}
        self.students = students

    def to_dict(self):
        students = {cur_stud_uid:self.students[cur_stud_uid].to_dict() for cur_stud_uid in self.students}
        return {"name": self.name, "spec": self.speciality, "year": self.start_year, "students": students}

    def __repr__(self):
        return "{name} ({year}, {spec})".format(name=self.name, year=self.start_year, spec=self.speciality)


class Task(FromToDict):
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


class TaskOption(FromToDict):
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


class TasksPool(FromToDict):
    """A set of tasks to choose the tasks for a particular assessment from"""

    def __init__(self, assessment_desciption=None):
        """
        Create a new task pool from xml
        :param assessment_desciption: a xml to create tasks pool from
        """
        self.threshold = 0.05
        self.name = ""
        self.time_per_task = 60
        self.tasks = []
        self.tasks_num = 12

        if not assessment_desciption:
            return

        xml_file = open(assessment_desciption, encoding="utf-8")
        text = xml_file.readlines()
        xml_file.close()

        soup = BeautifulSoup(" ".join(text), "xml")

        self.name = soup.findAll("Test")[0].attrs["name"]

        for task in soup.findAll("Question"):
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

    def create_test(self, tasks_num, student=None):
        """
        Create new assessment
        :param tasks_num: the number of the tasks in the newly creating assessment
        :param student: a student the assessment is creating for
        :return: new assessment from tasks pool for the given student
        """
        if tasks_num <= 0:
            raise ValueError("Wrong number of the tasks in the assessment: \
            the number of tasks can't be zero or negative")

        if tasks_num > len(self.tasks):
            raise ValueError("Wrong number of the tasks in the assessment: greater than tasks in task pool")

        new_assessment = Assessment()
        new_assessment.name = self.name
        new_assessment.time_limit = self.tasks_num * self.time_per_task
        new_assessment.student = student
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

        attempts_num = 0
        while attempts_num < 5:
            assessments = []
            for i in range(assessments_num):
                assessments.append(assesst(items_num=len(tasks), assesst_props=descr, choice=True))

            values = np.unique(assessments)
            values1 = np.append(values, [1.1])

            hist, bins = np.histogram(assessments, bins=values1)

            hist_sum = np.sum(hist)

            hist = list(hist / float(hist_sum))

            elem_sum = 0
            index = 0
            hist.reverse()

            step_found = True
            for i, elem in enumerate(hist):
                elem_sum += elem
                if hist[i] >= hist[i + 1]:
                    step_found = False
                    break

                if elem_sum > self.threshold:
                    index = i
                    break

            new_assessment.threshold = values[-(index + 1)] * 100
            if index != 0 and step_found:
                break

            attempts_num += 1

        return new_assessment

    def to_dict(self):
        dict_to_export = {}
        dict_to_export.update({'name': self.name, 'time_per_task': self.time_per_task, 'threshold': self.threshold})
        tasks = [cur_task.to_dict() for cur_task in self.tasks]
        dict_to_export.update({'tasks': tasks})

        return dict_to_export

    def from_dict(self, descr):
        self.name = descr['name']
        self.time_per_task = descr['time_per_task']
        self.threshold = descr['threshold']
        self.tasks = []
        for cur_task_descr in descr['tasks']:
            new_task = Task()
            new_task.from_dict(cur_task_descr)
            self.tasks.append(new_task)

    def __repr__(self):
        return "{name} ({qnum})".format(name=self.name, qnum=len(self.tasks))


class Assessment(FromToDict):
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
        self.mistaken_tasks = []
        self.score = 0
        self.real_score = 0
        self.uuid = uuid.uuid4().hex

    def get_score(self, answers):
        """
        Calculate the score for the given answer
        :param answers: a set of checked uuids (the options for the tasks)
        :return: the final score from 0 to 100, the assessment threshold, the calculated score
        """
        if not isinstance(answers, set):
            raise ValueError("The answers should be a set of uuids.")

        self.checked_uuids = copy.copy(answers)

        all_options = self.answers_uuids.union(self.distractors_uuids)
        not_checked = all_options.difference(answers)

        self.score = float(len(self.answers_uuids & answers) + len(self.distractors_uuids & not_checked)) / \
                float(len(all_options)) * 100.0
        self.real_score = (self.score - self.threshold) / (100 - self.threshold) * 100.0
        self.real_score = self.real_score if self.real_score > 0 else 0

        self.checked_uuids = answers

        self.mistaken_uuids = self.distractors_uuids.intersection(self.checked_uuids).\
            union(self.answers_uuids.difference(self.checked_uuids))

        for cur_mistake in self.mistaken_uuids:
            for cur_task in self.tasks:
                if cur_mistake in map(lambda x: x["uuid"], cur_task["options"]):
                    if cur_task not in self.mistaken_tasks:
                        self.mistaken_tasks.append(cur_task)

        return self.real_score, self.threshold, self.score

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
