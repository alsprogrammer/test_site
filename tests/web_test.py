import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import threading

from flask_app import app


class Test(unittest.TestCase):
    def server_run(self):
        app.run(debug=True, use_reloader=False)

    def setUp(self):
        self.server_thread = threading.Thread(target=self.server_run)
        self.server_thread.daemon = True
        self.server_thread.start()

        self.driver = webdriver.Firefox(executable_path='f:\\Projects\\web\\geckodriver.exe')

    def test_group_create(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000")
        self.assertIn("Alexander Sayapin", driver.page_source)
        #elem = driver.find_element_by_name("q")
        #elem.send_keys("pycon")
        #assert "No results found." not in driver.page_source
        #elem.send_keys(Keys.RETURN)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
