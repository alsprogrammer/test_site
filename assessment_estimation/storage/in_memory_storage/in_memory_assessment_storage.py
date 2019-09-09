from typing import Coroutine, Generator
from assessment_estimation.storage.storage_abc import AsssessmentStorage, StudentStorage
from assessment_estimation.storage.in_memory_storage.persistent_converters.file_converter import FileStorage
from assessment_estimation.subjects import Assessment


class InMemoryAssessmentStorage(AsssessmentStorage):
    def __init__(self):
        self.assessment_dict = {}

    def get_by_id(self, assessment_id) -> Assessment:
        return self.assessment_dict.get(assessment_id)

    def upsert(self, assessment_to_save: Assessment):
        self.assessment_dict[assessment_to_save.uuid] = assessment_to_save

    def persist(self, coder: Coroutine[Assessment, None, None]):
        coder.__next__()
        for cur_assessment_uid in self.assessment_dict:
            coder.send(self.assessment_dict[cur_assessment_uid])
        coder.close()

    def restore(self, decoder: Generator[Assessment, None, None]):
        for cur_assessment in decoder:
            self.assessment_dict[cur_assessment.uuid] = cur_assessment


def assessment_xml_converter(assessment: Assessment) -> str:
    return assessment.uuid


if __name__ == "__main__":
    assessment_storage = InMemoryAssessmentStorage()
    assessment = Assessment()
    assessment_storage.upsert(assessment)

    file_coder = FileStorage.persist("/tmp/assessment_file.xml", assessment_xml_converter)

    assessment_storage.persist(file_coder)
