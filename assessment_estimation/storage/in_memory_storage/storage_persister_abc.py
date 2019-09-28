from abc import ABC, abstractmethod

from assessment_estimation.storage.storages_abc import Storage


class StoragePersister(ABC):
    @abstractmethod
    def persist(self, storage: Storage, file_name: str):
        pass

    @abstractmethod
    def restore(self, storage: Storage, file_name: str):
        pass
