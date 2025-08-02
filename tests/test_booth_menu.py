import unittest
from booth_menu import BoothMenu
from selenium.webdriver.remote.webelement import WebElement



class TestBoothMenu(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bm = BoothMenu()


    @classmethod
    def tearDownClass(cls):
        cls.bm.terminate()


    def test_find_booth_position(self):        
        booth_position = self.bm.find_booth_position(id=3)
        
        print(booth_position)

        self.assertIsInstance(booth_position, WebElement)


    def test_scrolling_menu(self):
        self.bm.scroll_a_bit()