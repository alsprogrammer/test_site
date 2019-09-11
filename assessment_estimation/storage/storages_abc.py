from abc import ABC, abstractmethod
from typing import List
from assessment_estimation.subjects import Model, Student, Group, Task


class Storage(ABC):
    @abstractmethod
    def get_by_id(self, id: str) -> Model:
        pass

    @abstractmethod
    def upsert(self, object_to_upsert: Model):
        pass


class StudentStorage(Storage, ABC):
    @abstractmethod
    def get_all(self) -> List[Student]:
        pass


class GroupStorage(Storage, ABC):
    @abstractmethod
    def get_by_year(self, year: int) -> List[Group]:
        pass

    @abstractmethod
    def get_by_speciality(self, speciality_name: str) -> List[Group]:
        pass


class AssessmentStorage(Storage, ABC):
    def get_by_id(self, id: str) -> Model:
        pass

    def upsert(self, object_to_upsert: Model):
        pass


class TaskStorage(Storage, ABC):
    @abstractmethod
    def get_by_topic(self, topic_name: str) -> List[Task]:
        pass

    @abstractmethod
    def get_topic_names(self, topic_name: str) -> List[str]:
        pass
