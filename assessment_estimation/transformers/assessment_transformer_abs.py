from abc import ABC, abstractmethod
from assessment_estimation.subjects import Assessment


class AssessmentTransformer(ABC):
    @abstractmethod
    def transform(self, assessment_to_transform: Assessment):
        pass
