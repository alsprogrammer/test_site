import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Test(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_group_create(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/admin/group/new")
        self.assertIn("Python", driver.title)
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        assert "No results found." not in driver.page_source
        elem.send_keys(Keys.RETURN)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
