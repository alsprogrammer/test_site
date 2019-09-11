from typing import Any, Generator, Coroutine, Iterable, List, Dict, Callable
from xml.etree import ElementTree as ET

from assessment_estimation.storage.in_memory_storage.xml_persistence import XMLFileStorage
from assessment_estimation.subjects import Model, Assessment, Group, Task, Student
from assessment_estimation.storage.storages_abc import AssessmentStorage, GroupStorage, TaskStorage, StudentStorage
from assessment_estimation.storage.in_memory_storage.in_memory_storage_abc import PersistableStorage
from assessment_estimation.storage.in_memory_storage.in_memory_storage_abc import element_pusher
from assessment_estimation.storage.in_memory_storage.in_memory_storage_abc import element_popper


class InMemoryAssessmentStorage(PersistableStorage, AssessmentStorage):
    pass


class InMemoryGroupStorage(PersistableStorage, GroupStorage):
    def get_by_speciality(self, speciality_name: str) -> List[Group]:
        return [self.elements_dict[cur_element_id] for cur_element_id in self.elements_dict
                if self.elements_dict[cur_element_id].speciality == speciality_name]

    def get_by_year(self, year: int) -> List[Group]:
        return [self.elements_dict[cur_element_id] for cur_element_id in self.elements_dict
                if self.elements_dict[cur_element_id].start_year == year]


class InMemoryTaskStorage(PersistableStorage, TaskStorage):
    def get_by_topic(self, topic_name: str) -> List[Task]:
        return [self.elements_dict[cur_element_id] for cur_element_id in self.elements_dict
                if self.elements_dict[cur_element_id].theme == topic_name]

    def get_topic_names(self, topic_name: str) -> List[str]:
        return list(set([self.elements_dict[cur_element_id].theme for cur_element_id in self.elements_dict]))


class InMemoryStudentStorage(StudentStorage, PersistableStorage):
    def get_all(self) -> List[Student]:
        return self.elements_dict.items()


def assessment2dict(assessment: Assessment) -> Dict:
    return {"id": assessment.uuid}


def xml2assessment_generator(dict_to_transform: ET.Element) -> Model:
    cur_assessment = Assessment()
    cur_assessment.from_dict(dict_to_transform.attrib)
    return cur_assessment


if __name__ == "__main__":
    xml_filename = "/tmp/filename.xml"

    assessment_storage = InMemoryAssessmentStorage()
    assessment = Assessment()
    assessment_storage.upsert(assessment)

    xml_file = XMLFileStorage(xml_filename, "Tests", "Test", assessment2dict)
    xml_coder = element_pusher(xml_file)
    assessment_storage.persist(xml_coder)
    xml_file.close()

    tree = ET.parse(xml_filename)
    root = tree.getroot()
    xml_decoder = element_popper(root, xml2assessment_generator)
    assessment_storage.restore(xml_decoder)

    print(root.tag)
    print(root.attrib)
    for child in root:
        print(child.tag, child.attrib)
