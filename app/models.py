from bs4 import BeautifulSoup

ROLE_USER = 0
ROLE_ADMIN = 1


class Student:
    def __init__(self):
        self.first_name = ""
        self.sur_name = ""
        self.last_name = ""
        self.group = None


class Group:
    def __init__(self):
        self.speciality = ""
        self.start_year = -1;
        self.name = ""
        self.students = []

    def __init__(self, speciality, year, name):
        self.speciality = speciality
        self.start_year = year
        self.name = name
        self.students = []

    def add_student(self, student):
        self.students.append(student)
        student.group = self


class TestSet:
    def __init__(self, xml_text):
        self.test_soup = BeautifulSoup(xml_text, "xml")

    def __getitem__(self, item):
        return self.test_soup.TestSet.findAll("Test")[item]


class TestingStudent:
    def __init__(self):
        self.test_bs = None
        self.student = None

    def __init__(self, student, test_bs):
        self.test_bs = test_bs
        self.student = student
