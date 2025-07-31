from selenium import webdriver
from selenium.webdriver.common.by import By
# from time import sleep


class BoothScraper:
    """
    A class to handle the scraping of booth data from ExpoFP.
    """

    def __init__(self, url: str ='') -> None:
        self.url = url
        self._driver = None
        self.shadow_root = None
        self.booths_div = None
        self.booth = None
        self.close_booth_button = None


    # this method is used to process url and initalize driver
    def open_url(self) -> webdriver.Chrome:
        """
        Opens the specified URL in a Chrome browser and initializes the driver.
        :return: The initialized    webdriver.Chrome instance.
        """
        self._driver = webdriver.Chrome()  # Initialize the Chrome driver
        self._driver.get(self.url)  # Open the specified URL
        return self._driver


    def find_shadow_root(self) -> None:
        """
        Moves the driver to the shadow root of the page.
        """

        if not self._driver:
            raise ValueError("Driver is not initialized. Call open_url() first.")
        
        shadow_host = self._driver.find_element(By.CSS_SELECTOR, 'div.expofp-floorplan > div')

        self.shadow_root = self._driver.execute_script("return arguments[0].shadowRoot", shadow_host)


    def find_booths_div(self) -> None:
        """Finds booths div within the shadow root."""

        overlay_content_scrollable = self._overlay_content_scrollable()
        
        virtual_scroll = overlay_content_scrollable.find_element(By.CSS_SELECTOR, 'div[style="height: 100%; cursor: pointer; resize: both; min-height: 100px;"]')
        
        self.booths_div = virtual_scroll.find_element(By.CSS_SELECTOR, 'div[data-virtuoso-scroller="true"] > div > div')


    def find_close_booth_button(self) -> None:
        """
        Finds the close button in booth details.
        """        
        self.close_booth_button = None

        overlay_bar = self._overlay_bar()
        
        overlay_bar_close = overlay_bar.find_element(By.CSS_SELECTOR, 'div.overlay-bar__close')
        
        self.close_booth_button = overlay_bar_close.find_element(By.CSS_SELECTOR, 'button')


    def _extract_name(self):
        overlay_bar = self._overlay_bar()
        return overlay_bar.find_element(By.CSS_SELECTOR, 'div.overlay-bar__slot').text


    def count_of_booths(self) -> int:
        """
        Returns the count of visible booths in the shadow root.
        """
        if not self.booths_div:
            raise ValueError("Booth block is not initialized. Call find_booths_div() first.")

        items = self.booths_div.find_elements(By.CSS_SELECTOR, 'div[data-index]')
        
        return len(items)
    
    
    def find_booth(self, id: int = 0):
        """Finds the booth in booths_div by id"""
        self.booth = None

        """Gets a booth element by its ID."""
        if not self.booths_div:
            raise ValueError("Booth block is not initialized. Call find_booths_div() first.")

        elements = self.booths_div.find_elements(By.CSS_SELECTOR, f'div[data-index="{id}"]')
        
        if elements:
            self.booth = elements[0]


    def extract_company_details(self) -> dict:
        """
        Returns the dict: {'name': '...', 'description': '...', 'address': '...', 'phone': '...', 'website': '...', 'email': ''...}
        from the opened booth. Before calling this method you have to call: 'booth.click()'.
        """
        company_details = {
            'name': '',
            'description': '',
            'address': '',
            'phone': '',
            'website': '',
            'email': '',
        }

        company_details['name'] = self._extract_name()

        exibitor_details = self._exibitor_details()
        # extracting description
        if exibitor_details:
            exibitor_description = exibitor_details.find_elements(By.CSS_SELECTOR, 'div.exhibitor-description')
            
            if exibitor_description:
                company_details['description'] = exibitor_description[0].text


        # extracting address, phone, website, email
        if exibitor_details:
            exibitor_meta = exibitor_details.find_elements(By.CSS_SELECTOR, 'div.exhibitor-meta')
            
            meta_block = None
            
            if exibitor_meta:
                meta_block = exibitor_meta[0]
            if meta_block:
                exibitor_meta_items = meta_block.find_elements(By.CSS_SELECTOR, 'div.exhibitor-meta__item')
            
                company_details['address'] = exibitor_meta_items[0].text if len(exibitor_meta_items) > 0 else ''
                company_details['phone'] = exibitor_meta_items[1].text if len(exibitor_meta_items) > 1 else ''
                company_details['website'] = exibitor_meta_items[2].text if len(exibitor_meta_items) > 2 else ''
                company_details['mail'] = exibitor_meta_items[3].text if len(exibitor_meta_items) > 3 else ''
        
        return company_details


    def terminate(self):
        """
        Terminates the driver 'self._driver.quit()' and resets self._driver = None. Run it after finishing of scraping.
        """
        if self._driver:
            self._driver.quit()
            self._driver = None  # Reset the driver to None after quitting


    def scroll_a_bit(self, pixels : int = 100):
        """
        Scrolls DOWN booths in booths_div. Should be performed after closing of the scraped booth. Default scroll is 100px.
        """
        overlay_content_scrollable = self._overlay_content_scrollable()
        self.driver.execute_script(f"arguments[0].scrollTop = arguments[0].scrollTop + {pixels};", overlay_content_scrollable)


    def _overlay_content(self):
        if not self.shadow_root:
            raise ValueError("Shadow root position is not initialized. Call find_shadow_root() first.")
        
        efp_layout = self.shadow_root.find_element(By.CSS_SELECTOR, 'div#efp-layout')
        layout_fixed = efp_layout.find_element(By.CSS_SELECTOR, 'div.layout__fixed')
        overlay = layout_fixed.find_element(By.CSS_SELECTOR, 'div.overlay')
        
        return overlay.find_element(By.CSS_SELECTOR, 'div#overlay-content')
              

    def _overlay_bar(self):
        overlay_content = self._overlay_content()

        return overlay_content.find_element(By.CSS_SELECTOR, 'div.overlay-bar') # contains company_name and 
    

    def _overlay_content_scrollable(self):
        overlay_content = self._overlay_content()

        return overlay_content.find_element(By.CSS_SELECTOR, 'div.overlay-content__scrollable')


    def _exibitor_details(self):
        """ this div can contain all description, adress, phone, website, email"""
        overlay_content_scrollable = self._overlay_content_scrollable()

        exhibitor_details = overlay_content_scrollable.find_elements(By.CSS_SELECTOR, 'div.exhibitor__details')

        return exhibitor_details[0] if exhibitor_details else None
    

    @property
    def driver(self):
        return self._driver

