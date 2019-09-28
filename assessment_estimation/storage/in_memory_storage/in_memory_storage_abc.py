from abc import ABC, abstractmethod
from _io import _IOBase
from typing import Any, Callable, Dict
from assessment_estimation.storage.storages_abc import Storage
from assessment_estimation.models.models import Model


class InMemoryStorage(Storage, ABC, dict):
    pass
