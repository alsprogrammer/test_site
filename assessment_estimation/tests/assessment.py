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


if __name__ == "__main__":
    unittest.main()
