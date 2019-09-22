from typing import List, Dict
from xml.etree import ElementTree as ET

from assessment_estimation.storage.in_memory_storage.xml_persistence import XMLFile2Save
from assessment_estimation.models.models import Model, Assessment, Group, Task
from assessment_estimation.storage.storages_abc import AssessmentStorage, GroupStorage, TaskStorage, StudentStorage
from assessment_estimation.storage.in_memory_storage.in_memory_storage_abc import PersistableStorage


class InMemoryAssessmentStorage(PersistableStorage, AssessmentStorage):
    pass


class InMemoryStudentStorage(StudentStorage, PersistableStorage):
    pass


class InMemoryGroupStorage(PersistableStorage, GroupStorage):
    def get_by_speciality(self, speciality_name: str) -> List[Group]:
        return [self[cur_element_id] for cur_element_id in self
                if self[cur_element_id].speciality == speciality_name]

    def get_by_year(self, year: int) -> List[Group]:
        return [self[cur_element_id] for cur_element_id in self
                if self[cur_element_id].start_year == year]


class InMemoryTaskStorage(PersistableStorage, TaskStorage):
    def get_by_topic(self, topic_name: str) -> List[Task]:
        return [self[cur_element_id] for cur_element_id in self
                if self[cur_element_id].theme == topic_name]

    def get_topic_names(self, topic_name: str) -> List[str]:
        return list(set([self[cur_element_id].theme for cur_element_id in self]))


def dict2assessment(dict_to_transform: Dict) -> Model:
    cur_assessment = Assessment()
    cur_assessment.from_dict(dict_to_transform.attrib)
    return cur_assessment


if __name__ == "__main__":
    xml_filename = "/tmp/filename.xml"

    xml_file = XMLFile2Save(xml_filename, "Tests", "Test", dict2assessment)

    assessment_storage = InMemoryAssessmentStorage(xml_file, None)
    assessment = Assessment()
    assessment_storage[assessment.uuid] = assessment

    assessment_storage.persist()
    xml_file.close()

    tree = ET.parse(xml_filename)
    root = tree.getroot()
    xml_decoder = element_popper(root, xml2assessment_generator)
    assessment_storage.restore(xml_decoder)

    print(root.tag)
    print(root.attrib)
    for child in root:
        print(child.tag, child.attrib)
