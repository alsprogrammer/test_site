import os
from config import DATA_PATH

ROLE_USER = 0
ROLE_ADMIN = 1


class Student:
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

    def save_to_xml_file(self, file_name):
        source_xml = BeautifulSoup('<?xml version="1.0" encoding="utf-8" standalone="yes"?><group></group>', "xml")
        source_xml.group["speciality"] = self.speciality
        source_xml.group["start_year"] = self.start_year
        source_xml.group["name"] = self.name
        group_tag = source_xml.group
        for cur_student in self.students:
            student_tag = source_xml.new_tag("student")
            student_tag['first_name'] = cur_student.first_name
            student_tag['sur_name'] = cur_student.sur_name
            student_tag['last_name'] = cur_student.last_name

            source_xml.group.append(student_tag)

        with open(os.path.join(DATA_PATH, "out.txt"), "w") as out:
            out.write(source_xml.prettify("utf-8", "xml"))


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
        #self.test_soup = BeautifulSoup(xml_text, "xml")

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
