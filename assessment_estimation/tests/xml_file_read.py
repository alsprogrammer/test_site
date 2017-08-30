import unittest
from ..subjects import TasksPool


class Test(unittest.TestCase):
    def test_assessment_load(self):
        pool = TasksPool("./files/test1.xml")
        self.assertEqual(len(pool.tasks), 16)

    def test_assessment_create_0(self):
        pool = TasksPool("./files/test1.xml")
        with self.assertRaises(ValueError):
            pool.create_test(0)

    def test_assessment_create_more(self):
        pool = TasksPool("./files/test1.xml")
        with self.assertRaises(ValueError):
            pool.create_test(17)

    def test_assessment_create(self):
        tasks_num = 12
        pool = TasksPool("./files/test1.xml")
        assessment = pool.create_test(tasks_num)
        self.assertEqual(len(assessment.tasks), tasks_num)

    def test_assessment_images(self):
        pool = TasksPool("./files/test2.xml")

        self.assertEqual(len(pool.tasks), 2)

        self.assertEqual(len(pool.tasks[0].answers), 1)
        self.assertEqual(len(pool.tasks[1].answers), 1)
        self.assertEqual(len(pool.tasks[0].distractors), 1)
        self.assertEqual(len(pool.tasks[1].distractors), 1)

        self.assertEqual(pool.tasks[0].answers[0].text, u'<{v1, v2, v3, v4}, {(v1, v1), (v1, v2), (v1, v4), (v2, v2), (v2, v3), (v3, v1), (v3, v3), (v4, v1}, (v4, v2), (v4, v3)>')
        self.assertEqual(pool.tasks[0].distractors[0].text, u'<{v1, v2, v3, v4, v5}, {(v1, v2), (v2, v4), (v4, v2), (v3, v1)}>')

        self.assertTrue(pool.tasks[0].picture.startswith("iVBORw0KGgoAAAANSUhEUgAAAKAAAAC"))
        self.assertIs(pool.tasks[1].picture, None)


if __name__ == "__main__":
    unittest.main()
