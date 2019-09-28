from typing import List, Dict

from assessment_estimation.models.models import Model, Assessment, Group, Task
from assessment_estimation.storage.storages_abc import AssessmentStorage, GroupStorage, TaskStorage, StudentStorage
from assessment_estimation.storage.in_memory_storage.in_memory_storage_abc import InMemoryStorage


class InMemoryAssessmentStorage(InMemoryStorage, AssessmentStorage):
    pass


class InMemoryStudentStorage(InMemoryStorage, StudentStorage):
    pass


class InMemoryGroupStorage(InMemoryStorage, GroupStorage):
    def get_by_speciality(self, speciality_name: str) -> List[Group]:
        return [self[cur_element_id] for cur_element_id in self
                if self[cur_element_id].speciality == speciality_name]

    def get_by_year(self, year: int) -> List[Group]:
        return [self[cur_element_id] for cur_element_id in self
                if self[cur_element_id].start_year == year]


class InMemoryTaskStorage(InMemoryStorage, TaskStorage):
    def get_by_topic(self, topic_name: str) -> List[Task]:
        return [self[cur_element_id] for cur_element_id in self
                if self[cur_element_id].theme == topic_name]

    def get_topic_names(self, topic_name: str) -> List[str]:
        return list(set([self[cur_element_id].theme for cur_element_id in self]))


def dict2assessment(dict_to_transform: Dict) -> Model:
    cur_assessment = Assessment()
    cur_assessment.from_dict(dict_to_transform.attrib)
    return cur_assessment
