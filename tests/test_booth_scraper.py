import unittest
from booth_scraper import BoothScraper
from time import sleep


class TestBoothScraper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass


    @classmethod
    def tearDownClass(cls):
        pass


    def setUp(self):
        self.url = 'https://ice25.expofp.com/'
        self.scraper = BoothScraper(self.url)
        self.scraper.open_url()
        sleep(10)  # Allow time for the page to load before tests

    def tearDown(self):
        if self.scraper.driver:
            self.scraper.terminate()


    def test_scraper_initialization(self):
        self.assertIsNone(self.scraper.shadow_root, "Shadow root position should be None before moving to shadow root")
        self.assertIsNone(self.scraper.booths_div, "Booth block should be None before moving to booths block")
        self.assertIsNotNone(self.scraper.driver, "Driver should be not None after opening URL")
        self.assertEqual(self.scraper.url, self.url, "URL should match the initialized value")


    def test_open_and_terminate_scraper(self):
        self.new_scraper = BoothScraper(self.url)
        self.new_scraper.open_url()
        self.assertIsNotNone(self.new_scraper.driver, "Driver should be not None after opening URL")
        self.new_scraper.terminate()
        self.assertIsNone(self.new_scraper.driver, "Driver should be None after terminating the scraper")
        


    def test_driver_in_shadow_root(self):
        self.scraper.find_shadow_root()

        self.assertIsNotNone(self.scraper.shadow_root, "Shadow root position should not be None")


    def test_opening_booths_div(self):
        self.scraper.find_shadow_root()
        self.scraper.find_booths_div()

        self.assertGreater(self.scraper.count_of_booths(), 3, "There should be greater 3 booths in the booth block")
        

    def test_opening_booth_by_id(self):
        self.scraper.find_shadow_root()
        self.scraper.find_booths_div()
        self.scraper.find_booth(0)
        self.assertIsNotNone(self.scraper.booth, "Booth with ID 0 should not be None")
    #     time.sleep(5)
        self.scraper.booth.click()
        sleep(10)

    
    def test_opening_by_invalid_id(self):
        self.scraper.find_shadow_root()
        self.scraper.find_booths_div()

        self.scraper.find_booth(9999)
        self.assertIsNone(self.scraper.booth, "Booth with invalid ID should be None")

    
    def test_extract_company_details(self):
        self.assertIsNone(self.scraper.booth, "Booth should be None before clicking")
        self.assertIsNone(self.scraper.close_booth_button, "Close button should be None before clicking")

        self.scraper.find_shadow_root()
        self.scraper.find_booths_div()
        self.scraper.find_booth(0)
        self.scraper.booth.click()
        sleep(5)
        self.scraper.find_close_booth_button()
        self.assertIsNotNone(self.scraper.close_booth_button, "Close button should not be None after clicking booth")

        company_details = self.scraper.extract_company_details()

        self.assertIsInstance(company_details, dict, "Company details should be a dictionary")
    
        self.assertIn('name', company_details, "Company details should contain 'name'")
        self.assertIn('description', company_details, "Company details should contain 'description'")
        self.assertIn('address', company_details, "Company details should contain 'address'")
        self.assertIn('phone', company_details, "Company details should contain 'phone'")
        self.assertIn('website', company_details, "Company details should contain 'website'")
        self.assertIn('mail', company_details, "Company details should contain 'mail'")

        print(company_details)

        self.scraper.close_booth_button.click()
        sleep(5)

    def test_scroll_a_bit(self):
        self.scraper.find_shadow_root()
        self.scraper.scroll_a_bit(200)

