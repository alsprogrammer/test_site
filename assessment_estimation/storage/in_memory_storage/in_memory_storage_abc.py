from abc import ABC, abstractmethod
from typing import Any, Generator, Coroutine, Callable, Iterable, List
from assessment_estimation.storage.storages_abc import Storage
from assessment_estimation.subjects import Model

import xml.etree.ElementTree as ET


class InMemoryStorage(Storage, ABC):
    elements_dict = {}

    def get_by_id(self, id: str) -> Model:
        return self.elements_dict.get(id)

    def upsert(self, object_to_upsert: Model):
        self.elements_dict[object_to_upsert.uuid] = object_to_upsert


class PersistableStorage(InMemoryStorage, ABC):
    def persist(self, coder: Coroutine[Model, None, None]):
        coder.__next__()
        for cur_element_uid in self.elements_dict:
            coder.send(self.elements_dict[cur_element_uid])
        coder.close()

    def restore(self, decoder: Generator[Model, None, None]):
        for cur_element in decoder:
            self.elements_dict[cur_element.uuid] = cur_element


def element_pusher(iterable_to_append) -> Coroutine[Model, None, None]:
    try:
        while True:
            cur_model = (yield)
            iterable_to_append.append(cur_model)
    except GeneratorExit:
        pass


def element_popper(source: Iterable, converter: Callable[[Any], Model]) -> Generator[List[Model], None, None]:
    for element in source:
        yield converter(element)


class FileStorage(ABC):
    @abstractmethod
    def append(self, model_to_add: Model):
        pass

    @abstractmethod
    def close(self):
        pass
