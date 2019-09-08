from assessment_estimation.storage.storage_abc import AsssessmentStorage
from assessment_estimation.subjects import Assessment


class InMemoryAssessmentStorage(AsssessmentStorage):
    def __init__(self):
        self.assessment_dict = {}

    def get_by_id(self, assessment_id) -> Assessment:
        return self.assessment_dict.get(assessment_id)

    def upsert(self, assessment_to_save: Assessment):
        self.assessment_dict[assessment_to_save.uuid] = assessment_to_save
