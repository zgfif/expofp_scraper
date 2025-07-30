from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


class BoothScraper:
    """A class to handle the scraping of booth data from ExpoFP."""
    def __init__(self, url: str ='') -> None:
        self.url = url
        self._driver = None
        self.shadow_root = None
        self.booth_block = None
        self.booth = None
        self.close_button = None


    def open_url(self) -> webdriver.Chrome:
        """        Opens the specified URL in a Chrome browser and initializes the driver.
        :return: The initialized    webdriver.Chrome instance.
        """
        self._driver = webdriver.Chrome()  # Initialize the Chrome driver
        self._driver.get(self.url)  # Open the specified URL
        return self._driver


    def move_to_shadow_root(self) -> None:
        """Moves the driver to the shadow root of the page."""

        if not self._driver:
            raise ValueError("Driver is not initialized. Call open_url() first.")
        
        shadow_host = self._driver.find_element(By.CSS_SELECTOR, 'div.expofp-floorplan > div')
        self.shadow_root = self._driver.execute_script("return arguments[0].shadowRoot", shadow_host)


    def move_to_booths_block(self) -> None:
        """Moves the driver to the booths block within the shadow root."""
        if not self.shadow_root:
            raise ValueError("Shadow root position is not initialized. Call move_to_shadow_root() first.")
        
        efp_layout = self.shadow_root.find_element(By.CSS_SELECTOR, 'div#efp-layout')
        layout_fixed = efp_layout.find_element(By.CSS_SELECTOR, 'div.layout__fixed')
        overlay = layout_fixed.find_element(By.CSS_SELECTOR, 'div.overlay')
        overlay_content = overlay.find_element(By.CSS_SELECTOR, 'div#overlay-content')
        scrollable = overlay_content.find_element(By.CSS_SELECTOR, 'div.overlay-content__scrollable')
        virtual_scroll = scrollable.find_element(By.CSS_SELECTOR, 'div[style="height: 100%; cursor: pointer; resize: both; min-height: 100px;"]')
        
        self.booth_block = virtual_scroll.find_element(By.CSS_SELECTOR, 'div[data-virtuoso-scroller="true"] > div > div')


    def get_close_button(self):
        """Finds the close button in booth details."""
        
        self.close_button = None
        
        if not self.shadow_root:
            raise ValueError("Shadow root position is not initialized. Call move_to_shadow_root() first.")

        efp_layout = self.shadow_root.find_element(By.CSS_SELECTOR, 'div#efp-layout')
        layout_fixed = efp_layout.find_element(By.CSS_SELECTOR, 'div.layout__fixed')
        overlay = layout_fixed.find_element(By.CSS_SELECTOR, 'div.overlay')
        overlay_content = overlay.find_element(By.CSS_SELECTOR, 'div#overlay-content')
        overlay_bar = overlay_content.find_element(By.CSS_SELECTOR, 'div.overlay-bar')
        overlay_bar_close = overlay_bar.find_element(By.CSS_SELECTOR, 'div.overlay-bar__close')
        self.close_button = overlay_bar_close.find_element(By.CSS_SELECTOR, 'button')


    def count_of_booths(self) -> int:
        """Counts the number of booths in the shadow root."""
        if not self.booth_block:
            raise ValueError("Booth block is not initialized. Call move_to_booths_block() first.")

        items = self.booth_block.find_elements(By.CSS_SELECTOR, 'div[data-index]')
        
        return len(items)
    
    
    def get_booth_by_id(self, id: int = 0):
        self.booth = None

        """Gets a booth element by its ID."""
        if not self.booth_block:
            raise ValueError("Booth block is not initialized. Call move_to_booths_block() first.")

        elements = self.booth_block.find_elements(By.CSS_SELECTOR, f'div[data-index="{id}"]')
        
        if elements:
            self.booth = elements[0]
        
        return self.booth


    def extract_company_details(self) -> dict:
        company_details = {
            'name': '',
            'description': '',
            'address': '',
            'phone': '',
            'website': '',
            'email': '',
        }

        """Extracts company details from the booth."""
        efp_layout = self.shadow_root.find_element(By.CSS_SELECTOR, 'div#efp-layout')
        layout_fixed = efp_layout.find_element(By.CSS_SELECTOR, 'div.layout__fixed')
        overlay = layout_fixed.find_element(By.CSS_SELECTOR, 'div.overlay')
        overlay_content = overlay.find_element(By.CSS_SELECTOR, 'div#overlay-content')
        overlay_bar = overlay_content.find_element(By.CSS_SELECTOR, 'div.overlay-bar')
        
        company_details['name'] = overlay_bar.find_element(By.CSS_SELECTOR, 'div.overlay-bar__slot').text

        overlay_content = overlay.find_element(By.CSS_SELECTOR, 'div#overlay-content')
        overlay_content_scrollable = overlay_content.find_element(By.CSS_SELECTOR, 'div.overlay-content__scrollable')
        exhibitor_details = overlay_content_scrollable.find_elements(By.CSS_SELECTOR, 'div.exhibitor__details')
        
        if exhibitor_details:
            exhibitor_details = exhibitor_details[0]
        else:
            exhibitor_details = None
        
        if exhibitor_details:
            exibitor_description = exhibitor_details.find_elements(By.CSS_SELECTOR, 'div.exhibitor-description')
            
            if exibitor_description:
                company_details['description'] = exibitor_description[0].text


        if exhibitor_details:
            exibitor_meta = exhibitor_details.find_elements(By.CSS_SELECTOR, 'div.exhibitor-meta')
            
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
        if self._driver:
            self._driver.quit()
            self._driver = None  # Reset the driver to None after quitting


    def scroll_a_bit(self, pixels : int = 100):
        efp_layout = self.shadow_root.find_element(By.CSS_SELECTOR, 'div#efp-layout')
        layout_fixed = efp_layout.find_element(By.CSS_SELECTOR, 'div.layout__fixed')
        overlay = layout_fixed.find_element(By.CSS_SELECTOR, 'div.overlay')
        overlay_content = overlay.find_element(By.CSS_SELECTOR, 'div#overlay-content')
        scrollable = overlay_content.find_element(By.CSS_SELECTOR, 'div.overlay-content__scrollable')

        self.driver.execute_script(f"arguments[0].scrollTop = arguments[0].scrollTop + {pixels};", scrollable)


    @property
    def driver(self):
        return self._driver

