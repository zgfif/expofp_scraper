from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import time


class BoothPage():
    def __init__(self, booth_position: WebElement, driver: WebElement) -> None:
        self.booth_position = booth_position
        self._driver = driver

        self.booth_position.click()
        time.sleep(5)


    def extract_name(self) -> str:
        overlay_bar = self._overlay_bar()  
        return overlay_bar.find_element(By.CSS_SELECTOR, 'div.overlay-bar__slot').text
    

    def extract_close_button(self) -> WebElement:
        overlay_bar = self._overlay_bar()
        
        overlay_bar_close = overlay_bar.find_element(By.CSS_SELECTOR, 'div.overlay-bar__close')
        
        return overlay_bar_close.find_element(By.CSS_SELECTOR, 'button')
    

    def extract_description(self) -> str:
        description = ''
        
        exibitor_details = self._exhibitor_details()
        
        if exibitor_details:
            exibitor_description = exibitor_details.find_elements(By.CSS_SELECTOR, 'div.exhibitor-description')
            
            if exibitor_description:
                description = exibitor_description[0].text
        return description

      
    def extract_additional_details(self) -> dict:
        """extracting address, phone, website, email. returns dict"""
        icons = {
            'icon-marker-pin-solid': 'address',
            'icon-phone-solid': 'phone',
            'icon-globe-solid': 'website',
            'icon-mail-at-solid': 'email',
        }

        dct = {'address': '', 'phone': '', 'website': '', 'email': ''}
        
        exibitor_details = self._exhibitor_details() 
        
        if exibitor_details:
            exibitor_meta = exibitor_details.find_elements(By.CSS_SELECTOR, 'div.exhibitor-meta')
            
            meta_block = None
            
            if exibitor_meta:
                meta_block = exibitor_meta[0]
            if meta_block:
                exibitor_meta_items = meta_block.find_elements(By.CSS_SELECTOR, 'div.exhibitor-meta__item')

                for item in exibitor_meta_items:
                    container = item.find_element(By.CSS_SELECTOR, "div.exhibitor-meta__icon")
                    icon = container.find_element(By.TAG_NAME, "i")
                    icon_class = icon.get_attribute("class")
  
                    dct[icons[icon_class]] = item.text

        return dct
    

    def close(self) -> None:
        self.extract_close_button().click()


    def _overlay_bar(self) -> WebElement:
        overlay_content = self._overlay_content()

        return overlay_content.find_element(By.CSS_SELECTOR, 'div.overlay-bar') # contains company_name and 
  

    def _overlay_content(self) -> WebElement:
        shadow_root = self._shadow_root()
        
        efp_layout = shadow_root.find_element(By.CSS_SELECTOR, 'div#efp-layout')
        layout_fixed = efp_layout.find_element(By.CSS_SELECTOR, 'div.layout__fixed')
        overlay = layout_fixed.find_element(By.CSS_SELECTOR, 'div.overlay')
        
        return overlay.find_element(By.CSS_SELECTOR, 'div#overlay-content')
    

    def _exhibitor_details(self) -> WebElement|None:
        """ this div can contain all description, adress, phone, website, email"""
        overlay_content_scrollable = self._overlay_content_scrollable()

        exhibitor_details = overlay_content_scrollable.find_elements(By.CSS_SELECTOR, 'div.exhibitor__details')

        return exhibitor_details[0] if exhibitor_details else None
    

    def _overlay_content_scrollable(self) -> WebElement:
        overlay_content = self._overlay_content()

        return overlay_content.find_element(By.CSS_SELECTOR, 'div.overlay-content__scrollable')
   

    def _shadow_root(self) -> WebElement:
        """
        Moves the driver to the shadow root of the page.
        """
        shadow_host = self._driver.find_element(By.CSS_SELECTOR, 'div.expofp-floorplan > div')

        return self._driver.execute_script("return arguments[0].shadowRoot", shadow_host)
