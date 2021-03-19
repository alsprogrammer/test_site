from abc import ABC, abstractmethod
from typing import Iterable, Mapping
from assessment_estimation.models.models import Group, Task, TopicSet


class Storage(ABC, Mapping):
    pass


class StudentStorage(Storage, ABC):
    pass


class GroupStorage(Storage, ABC):
    @abstractmethod
    def get_by_year(self, year: int) -> Iterable[Group]:
        pass

    @abstractmethod
    def get_by_speciality(self, speciality_name: str) -> Iterable[Group]:
        pass


class AssessmentStorage(Storage, ABC):
    pass


class TaskStorage(Storage, ABC):
    @abstractmethod
    def get_by_topic(self, topic_name: str) -> Iterable[Task]:
        pass

    @abstractmethod
    def get_topic_names(self, topic_name: str) -> Iterable[str]:
        pass


class TopicSetsStorage(Storage, ABC):
    @abstractmethod
    def get_by_topic_uid_in(self, topic_uid: str) -> Iterable[TopicSet]:
        pass
