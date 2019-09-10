from abc import ABC, abstractmethod
from typing import Coroutine, Generator
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


class PersistableStorage:
    elements_dict = {}

    def persist(self, coder: Coroutine[Model, None, None]):
        coder.__next__()
        for cur_element_uid in self.elements_dict:
            coder.send(self.elements_dict[cur_element_uid])
        coder.close()

    def restore(self, decoder: Generator[Model, None, None]):
        for cur_element in decoder:
            self.elements_dict[cur_element.uuid] = cur_element


class GroupStorage(Storage, ABC):
    @abstractmethod
    def get_by_year(self, year: int) -> List[Group]:
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
