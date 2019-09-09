from abc import ABC, abstractmethod
from typing import List
from assessment_estimation.subjects import Student, Group, Assessment, Task


class StudentStorage(ABC):
    @abstractmethod
    def get_by_id(self, student_id) -> Student:
        pass

    @abstractmethod
    def get_by_group_id(self, group_id) -> List[Student]:
        pass

    @abstractmethod
    def upsert(self, student_to_save: Student):
        pass

    @abstractmethod
    def get_all(self) -> List[Student]:
        pass


class GroupStorage(ABC):
    @abstractmethod
    def get_by_id(self, group_id) -> Group:
        pass

    @abstractmethod
    def get_by_year(self, year: int) -> List[Group]:
        pass

    @abstractmethod
    def upsert(self, group_to_save: Group):
        pass


class AsssessmentStorage(ABC):
    @abstractmethod
    def get_by_id(self, assessment_id):
        pass

    @abstractmethod
    def upsert(self, assessment_to_save: Assessment):
        pass


class TaskStorage(ABC):
    @abstractmethod
    def get_by_id(self, task_id) -> Task:
        pass

    @abstractmethod
    def get_by_topic(self, topic_name: str) -> List[Task]:
        pass

    @abstractmethod
    def get_topic_names(self, topic_name: str) -> List[str]:
        pass
