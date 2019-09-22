from typing import List

from assessment_estimation.models.models import Group, Student
from assessment_estimation.storage.storages_abc import StudentStorage, GroupStorage


class StudentService:
    def __init__(self, student_storage: StudentStorage, group_storage: GroupStorage):
        self._student_storage = student_storage
        self._group_storage = group_storage

    def create_student(self, first_name: str, sur_name: str, last_name: str, group_uid: str):
        if group_uid not in self._group_storage:
            raise KeyError()

        group = self._group_storage[group_uid]
        student = Student(last_name, first_name, sur_name, group)
        self._student_storage[student.uuid] = student

    def create_group(self, speciality: str, creation_year: int, name: str, student_names: List[str]):
        if name in [group.name for group in self._group_storage]:
            raise NameError('The group with the name {} already exists'.format(name))

        group = Group(speciality, creation_year, name)
        self._group_storage[group.uuid] = group

    def delete_student(self, student_uid: str):
        if student_uid not in self._student_storage:
            raise KeyError()

        student = self._student_storage[student_uid]

        del student.group.students[student_uid]
        del self._student_storage[student_uid]

    def delete_group(self, group_uid: str):
        if group_uid not in self._group_storage:
            raise KeyError()

        group = self._group_storage[group_uid]
        student_uids_list = group.students.keys()
        for student_uid in student_uids_list:
            del group.students[student_uid]
        del self._group_storage[group_uid]

    def put_student_to_group(self, student_uid: str, group_uid: str):
        if group_uid not in self._group_storage:
            raise KeyError()
        if student_uid not in self._student_storage:
            raise KeyError()

        group = self._group_storage[group_uid]
        student = self._student_storage[student_uid]
        student_group = student.group

        student.group = group
        if student_uid not in group.students.keys():
            group.add_student(student)

        if student_group is not None and student_group != group:
            del student_group[student_uid]
