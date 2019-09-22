from abc import ABC, abstractmethod
from collections import abc
from typing import List
from assessment_estimation.models.models import Group, Task


class Storage(ABC, abc.MutableMapping):
    pass


class StudentStorage(Storage, ABC):
    pass


class GroupStorage(Storage, ABC):
    @abstractmethod
    def get_by_year(self, year: int) -> List[Group]:
        pass

    @abstractmethod
    def get_by_speciality(self, speciality_name: str) -> List[Group]:
        pass


class AssessmentStorage(Storage, ABC):
    pass


class TaskStorage(Storage, ABC):
    @abstractmethod
    def get_by_topic(self, topic_name: str) -> List[Task]:
        pass

    @abstractmethod
    def get_topic_names(self, topic_name: str) -> List[str]:
        pass
