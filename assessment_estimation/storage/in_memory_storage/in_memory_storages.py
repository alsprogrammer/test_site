from abc import ABC
from typing import Generator, Coroutine
from assessment_estimation.storage.storages_abc import Storage, AssessmentStorage
from assessment_estimation.storage.in_memory_storage.persistent_converters.file_converter import FileStorage
from assessment_estimation.subjects import Model, Assessment


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


class InMemoryAssessmentStorage(PersistableStorage, AssessmentStorage):
    pass


def assessment_xml_converter(assessment: Assessment) -> str:
    return assessment.uuid


if __name__ == "__main__":
    assessment_storage = InMemoryAssessmentStorage()
    assessment = Assessment()
    assessment_storage.upsert(assessment)

    file_coder = FileStorage.persist("f:/Test/assessment_file.xml", assessment_xml_converter)

    assessment_storage.persist(file_coder)
