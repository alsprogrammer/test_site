from abc import ABC, abstractmethod
from _io import _IOBase
from typing import Any, Callable, Dict
from assessment_estimation.storage.storages_abc import Storage
from assessment_estimation.models.models import Model


class FileLike(ABC, _IOBase):
    pass


class InMemoryStorage(Storage, ABC, dict):
    pass


class PersistableStorage(InMemoryStorage, ABC):
    @staticmethod
    def _object2dict(obj: Any, class_key=None) -> Dict[str, Any]:
        """
        Convert any object to dict
        This part of the code is taken from the repository https://gist.github.com/sungitly/3f75cb297572dace2937
        :param obj: object to convert to dict
        :param class_key:
        :return: the dictionary that represents the object
        """
        if isinstance(obj, dict):
            data = {}
            for (k, v) in obj.items():
                data[k] = PersistableStorage._object2dict(v, class_key)
            return data
        elif hasattr(obj, "_ast"):
            return PersistableStorage._object2dict(obj._ast())
        elif hasattr(obj, "__iter__"):
            return [PersistableStorage._object2dict(v, class_key) for v in obj]
        elif hasattr(obj, "__dict__"):
            data = dict([(key, PersistableStorage._object2dict(value, class_key))
                         for key, value in obj.__dict__.items()
                         if not callable(value) and not key.startswith('_') and key not in ['name']])
            if class_key is not None and hasattr(obj, "__class__"):
                data[class_key] = obj.__class__.__name__
            return data
        else:
            return obj

    def __init__(self, file: FileLike, dict2object: Callable[[dict], Model]):
        self._converter = dict2object
        self._inner_storage = file

    def persist(self):
        for (key, value) in self.items():
            self._inner_storage.write(self._converter(value))
        self._inner_storage.flush()

    def restore(self):
        for cur_element in self._inner_storage:
            entity = self._converter(cur_element)
            self[entity.uuid] = entity
