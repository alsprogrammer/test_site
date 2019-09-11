from typing import Generator, Coroutine, Iterable, List, Dict

from assessment_estimation.subjects import Model, Assessment, Group, Task, Student
from assessment_estimation.storage.storages_abc import AssessmentStorage, GroupStorage, TaskStorage, StudentStorage
from assessment_estimation.storage.in_memory_storage.in_memory_storage_abc import PersistableStorage


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


def assessment_xml_converter(assessment: Assessment) -> str:
    return assessment.uuid


def xml2dict_generator(source: Iterable, converter) -> Generator[List[Model], None, None]:
    for xml_child in source:
        yield converter(xml_child.attrib)


def dict2assessment_generator(dict_to_transform: Dict) -> Model:
    cur_assessment = Assessment()
    cur_assessment.from_dict(dict_to_transform)
    return cur_assessment


if __name__ == "__main__":
    assessment_storage = InMemoryAssessmentStorage()
    assessment = Assessment()
    assessment_storage.upsert(assessment)

    file_coder = FileStorage.persist("/tmp/1.xml", assessment_xml_converter)

    assessment_storage.persist(file_coder)

    xml_string = """<?xml version="1.0" encoding="UTF-8"?>
<Test createdate="12.03.2018 11:22:17" discipline="Дискретная математика ТБ 090106" name="dm_block1">
  <Question number="0" theme="Множество">
    <Text>Принадлежит ли -10 множеству натуральных чисел?</Text>
    <Variant right="-">
      <Text>да</Text>
    </Variant>
    <Variant right="+">
      <Text>нет</Text>
    </Variant>
  </Question>
  <Question number="1" theme="Множество">
    <Text>Принадлежит ли 2 множеству целых чисел?</Text>
    <Variant right="+">
      <Text>да</Text>
    </Variant>
    <Variant right="-">
      <Text>нет</Text>
    </Variant>
  </Question>
</Test>
    """

    print(xml_string)
    # tree = ET.ElementTree(ET.fromstring(xml_string))
    tree = ET.parse("/tmp/2.xml")
    root = tree.getroot()
    xml_decoder = xml2dict_generator(root, dict2assessment_generator)
    assessment_storage.restore(xml_decoder)

    print(root.tag)
    print(root.attrib)
    for child in root:
        print(child.tag, child.attrib)
