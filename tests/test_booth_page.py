import unittest
from booth_menu import BoothMenu
from booth_page import BoothPage
from selenium.webdriver.remote.webelement import WebElement


class TestBoothPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('performs one time')
        cls.bm = BoothMenu()

        position = cls.bm.find_booth_position(id=3)

        cls.bp = BoothPage(booth_position=position, driver=cls.bm._driver)


    @classmethod
    def tearDownClass(cls):
        cls.bm.terminate()


    def test_extract_name(self):
        company_name = 'Angelina Yachtcharter'
        self.assertEqual(self.bp.extract_name(), company_name)


    def test_close_button(self):
        close_button =self.bp.extract_close_button()
        self.assertEqual(close_button.tag_name, 'button')
        self.assertIsInstance(close_button, WebElement)
            

    def test_extract_description(self):
        description = ''
        self.assertEqual(self.bp.extract_description(), description)


    def test_extract_addional_details(self):
        address = 'Kraljice Jelene\n3\nBiograd 23210\nCroatia'
        phone = '+38523385293'
        website = 'www.angelina.hr'
        email = 'info@angelina.hr'
        
        details = self.bp.extract_additional_details()
        
        self.assertEqual(details['address'], address)
        self.assertEqual(details['phone'], phone)
        self.assertEqual(details['website'], website)
        self.assertEqual(details['email'], email)

