from abc import ABC, abstractmethod

from assessment_estimation.models.models import Assessment


class Assessor(ABC):
    @abstractmethod
    def __call__(self, assessment: Assessment) -> float:
        pass
