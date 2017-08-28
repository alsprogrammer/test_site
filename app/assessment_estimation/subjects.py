from abc import ABCMeta, abstractmethod


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
        self.stem = ""
        self.picture = None
        self.answers = []
        self.distractors = []

    def __init__(self, stem, picture=None):
        self.stem = stem
        self.picture = picture

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

    def __repr__(self):
        return "{text}".format(text=self.stem)


class TaskOption(FromToDict):
    """Single task element - answer or distractor"""
    def __init__(self):
        self.text = ""
        self.picture = None

    def __init__(self, text, picture=None):
        self.text = text
        self.picture = picture


class TestSet:
    """ A set of tests.
    Contains a beautifulsoup xml description of the tests set.
    Single test xml description may be accessed through the number of  the test.
    """

    def __init__(self, xml_text):
        """Create a new test set from the xml test description

        Keyword arguments:
        xml_text - the xml test description to create test from
        """
        self.test_soup = BeautifulSoup(xml_text, "xml")

    def __getitem__(self, item):
        """Access the test by its number

        Keyword arguments:
        item - the number of the test to get
        """
        return self.test_soup.TestSet.findAll("Test")[item]


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
