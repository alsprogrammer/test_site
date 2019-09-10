from assessment_estimation.storage.storages_abc import Storage, PersistableStorage, AssessmentStorage
from assessment_estimation.storage.in_memory_storage.persistent_converters.file_converter import FileStorage
from assessment_estimation.subjects import Model, Assessment


class InMemoryStorage(Storage, PersistableStorage):
    def get_by_id(self, id: str) -> Model:
        return self.elements_dict.get(id)

    def upsert(self, element_to_save: Model):
        self.elements_dict[element_to_save.uuid] = element_to_save


class InMemoryAssessmentStorage(InMemoryStorage, AssessmentStorage):
    pass


def assessment_xml_converter(assessment: Assessment) -> str:
    return assessment.uuid


if __name__ == "__main__":
    assessment_storage = AssessmentStorage()
    assessment = Assessment()
    assessment_storage.upsert(assessment)

    file_coder = FileStorage.persist("/tmp/assessment_file.xml", assessment_xml_converter)

    assessment_storage.persist(file_coder)
