import unittest
from ..subjects import TasksPool


class Test(unittest.TestCase):
    def test_run_once(self):
        pool = TasksPool("./files/test1.xml")
        self.assertEqual(len(pool.tasks), 15)

if __name__ == "__main__":
    unittest.main()
