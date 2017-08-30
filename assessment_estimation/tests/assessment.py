import unittest
from ..subjects import TasksPool
import copy


class Test(unittest.TestCase):
    def test_assessment_100(self):
        pool = TasksPool("./files/test1.xml")
        assessment = pool.create_test(12, None)
        answers = set(copy.copy(assessment.answers_uuids))

        score, threshold, result = assessment.get_score(answers)
        self.assertEqual(score, 100)

    def test_assessment_0(self):
        pool = TasksPool("./files/test1.xml")
        assessment = pool.create_test(12, None)
        answers = set(copy.copy(assessment.distractors_uuids))

        score, threshold, result = assessment.get_score(answers)
        self.assertEqual(score, 0)

    def test_mistaken_uuids_and_tasks(self):
        pool = TasksPool("./files/test1.xml")
        assessment = pool.create_test(12, None)
        answers = set(copy.copy(assessment.distractors_uuids))

        assessment.get_score(answers)

        self.assertEqual(len(assessment.mistaken_tasks), 12)
        self.assertTrue(assessment.mistaken_uuids.issubset(assessment.distractors_uuids.union(assessment.answers_uuids)) and assessment.distractors_uuids.union(assessment.answers_uuids).issubset(assessment.mistaken_uuids), 0)


if __name__ == "__main__":
    unittest.main()
