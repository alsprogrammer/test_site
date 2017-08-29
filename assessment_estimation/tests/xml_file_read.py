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



if __name__ == "__main__":
    unittest.main()
