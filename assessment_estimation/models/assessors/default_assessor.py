from assessment_estimation.models.assessors.assesor_abc import Assessor
from assessment_estimation.models.models import Assessment


class DefaultAssessor(Assessor):
    def __call__(self, assessment: Assessment) -> float:
        """
        Calculate the score for the given assessment
        :param assessment: assessment to assest
        :return: the final score from 0 to 100, the assessment threshold, the calculated score
        """
        all_options = assessment.answers_uuids.union(assessment.distractors_uuids)
        not_checked = all_options.difference(assessment.checked_uuids)

        assessment.score = float(len(assessment.answers_uuids & assessment.checked_uuids) +
                           len(assessment.distractors_uuids & not_checked)) / \
            float(len(all_options)) * 100.0

        real_score = (assessment.score - assessment.threshold) / (100 - assessment.threshold) * 100.0
        assessment.real_score = real_score if real_score > 0 else 0

        assessment.mistaken_uuids = self.distractors_uuids.intersection(self.checked_uuids).\
            union(self.answers_uuids.difference(self.checked_uuids))

        for cur_mistake in assessment.mistaken_uuids:
            for cur_task in assessment.tasks:
                if cur_mistake in map(lambda x: x["uuid"], cur_task["options"]):
                    assessment.mistaken_tasks.append(cur_task)

        return assessment.real_score, assessment.threshold, assessment.score
