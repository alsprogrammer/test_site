from typing import Callable, Dict
from xml.etree import ElementTree as ET

from assessment_estimation.storage.in_memory_storage.in_memory_storage_abc import FileLike
from assessment_estimation.subjects import Model


class XMLFile2Save(FileLike):
    def __init__(self, filename_to_save: str, root_name: str, element_name: str,
                 model2dict_converter: Callable[[Model], Dict]):
        self._filename = filename_to_save
        self._tree = ET.Element(root_name)
        self.element_name = element_name
        self._converter = model2dict_converter

    def append(self, model_to_add: Model):
        model_dict = self._converter(model_to_add)
        xml_element = ET.Element(self.element_name)
        for attrib_name in model_dict:
            xml_element.set(attrib_name, model_dict[attrib_name])
        self._tree.append(xml_element)

    def close(self):
        tree = ET.ElementTree(self._tree)
        tree.write(self._filename)


class XMLFile2Read(FileLike):
    def close(self):
        pass

    def __iter__(self):
        pass
