from abc import ABC
from typing import Generator, Coroutine, List, Dict
from assessment_estimation.storage.storages_abc import Storage, AssessmentStorage
from assessment_estimation.storage.in_memory_storage.persistent_converters.file_converter import FileStorage
from assessment_estimation.subjects import Model, Assessment

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


class InMemoryAssessmentStorage(PersistableStorage, AssessmentStorage):
    pass


def assessment_xml_converter(assessment: Assessment) -> str:
    return assessment.uuid


def xml2dict_generator(filename) -> Generator[List[Dict], None, None]:
    xml_tree = ET.parse(filename)
    xml_root = xml_tree.getroot()
    for xml_child in xml_root:
        yield xml_child.attrib


def dict2assessment_generator(dict_generator) -> Generator[List[Model], None, None]:
    for cur_dict in dict_generator:
        cur_assessment = Assessment()
        cur_assessment.from_dict(cur_dict)
        yield cur_assessment


if __name__ == "__main__":
    assessment_storage = InMemoryAssessmentStorage()
    assessment = Assessment()
    assessment_storage.upsert(assessment)

    file_coder = FileStorage.persist("f:/Test/assessment_file.xml", assessment_xml_converter)

    assessment_storage.persist(file_coder)

    file_decoder = xml2dict_generator("f:/Test/1.xml")
    dict_decoder = dict2assessment_generator(file_decoder)
    assessment_storage.restore(dict_decoder)

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
    tree = ET.ElementTree(ET.fromstring(xml_string))
    root = tree.getroot()
    print(root.tag)
    print(root.attrib)
    for child in root:
        print(child.tag, child.attrib)
