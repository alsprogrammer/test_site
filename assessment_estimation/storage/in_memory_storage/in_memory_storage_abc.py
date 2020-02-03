from abc import ABC, abstractmethod
from assessment_estimation.storage.storages_abc import Storage


class InMemoryStorage(dict, Storage, ABC):
    pass
