import numbers
from _io import _IOBase
from typing import Callable, Dict, Any, Union, Set, List
from xml.dom import minidom

from xml.etree import ElementTree as ET

import xmlschema
from xmlschema import XMLSchema

from assessment_estimation.models.models import Model, Student, Group
from assessment_estimation.services.student_service import StudentService
from assessment_estimation.storage.in_memory_storage.in_memory_storages import InMemoryGroupStorage, \
    InMemoryStudentStorage
from assessment_estimation.storage.in_memory_storage.storage_persister_abc import StoragePersister
from assessment_estimation.storage.storages_abc import Storage


class XMLStoragePersister(StoragePersister):
    def __init__(self, filename: str, xml_schema: Union[str, _IOBase, XMLSchema],
                 dict_to_model_converter: Callable[[Dict], Model],
                 root_name: str, element_name: str):
        self._filename = filename
        self._converter = dict_to_model_converter
        self._xml_schema = xml_schema

        self._root_name = root_name
        self._element_name = element_name

    @staticmethod
    def _object2dict(obj: Any) -> Dict[str, Any]:
        return XMLStoragePersister._object2dict_impl(obj)

    @staticmethod
    def _object2dict_impl(obj: Any, class_key=None, converted_objects: List = None) -> Dict[str, Any]:
        """
        Convert any object to dict
        This part of the code is taken from the repository https://gist.github.com/sungitly/3f75cb297572dace2937
        :param obj: object to convert to dict
        :param class_key:
        :return: the dictionary that represents the object
        """
        if converted_objects is None:
            converted_objects = []

        if obj in converted_objects:
            return obj

        converted_objects.append(obj)

        if isinstance(obj, dict):
            data = {}
            for (k, v) in obj.items():
                data[k] = XMLStoragePersister._object2dict_impl(v, class_key, converted_objects)
            return data
        elif hasattr(obj, "_ast"):
            return XMLStoragePersister._object2dict_impl(obj._ast(), None, converted_objects)
        elif hasattr(obj, "__iter__") and not isinstance(obj, str):
            return [XMLStoragePersister._object2dict_impl(v, class_key, converted_objects) for v in obj]
        elif hasattr(obj, "__dict__"):
            data = dict([(key, XMLStoragePersister._object2dict_impl(value, class_key, converted_objects))
                         for key, value in obj.__dict__.items()
                         if not callable(value) and not key.startswith('_') and key not in ['name']])
            if class_key is not None and hasattr(obj, "__class__"):
                data[class_key] = obj.__class__.__name__
            return data
        else:
            return str(obj) if isinstance(obj, numbers.Number) else obj

    def persist(self, storage: Storage):
        tree = ET.Element(self._root_name)

        for cur_model_key in storage:
            model_to_add = storage[cur_model_key]
            model_dict = XMLStoragePersister._object2dict(model_to_add)
            xml_element = ET.Element(self._element_name)
            for attrib_name in model_dict:
                xml_element.set(attrib_name, model_dict[attrib_name])
            tree.append(xml_element)

        xmlstr = minidom.parseString(ET.tostring(tree)).toprettyxml(indent="   ")
        with open(self._filename, "w") as f:
            f.write(xmlstr)

    def restore(self, storage: Storage):
        xml_dict = xmlschema.to_dict(self._filename, self._xml_schema)

        for (key, value) in xml_dict.items():
            if key[0] == '@':
                continue
            model = self._converter(xml_dict[key])
            storage[model.uuid] = model


if __name__ == "__main__":

    group_storage = InMemoryGroupStorage()
    student_storage = InMemoryStudentStorage()
    student_service = StudentService(student_storage, group_storage)

    group = student_service.create_group("Прикладная математика", 2018, "БПМ18-01", [("Иван", "Иванович", "Иванов")])
    vrs = vars(group)

    xml_group_persister = XMLStoragePersister("/tmp/2.xml", None, None, "Group", "Student")
    xml_group_persister.persist(group_storage)
