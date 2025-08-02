from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from time import sleep


class BoothMenu():
    def __init__(self) -> None:
        self._driver = webdriver.Chrome()
        self._driver.get('https://ice25.expofp.com/')


    def find_booth_position(self, id=0) -> WebElement:
        virtual_scroll = self._overlay_content_scrollable().find_element(
            By.CSS_SELECTOR, 'div[style="height: 100%; cursor: pointer; resize: both; min-height: 100px;"]')
        # sleep(5)
        booths_div = virtual_scroll.find_element(By.CSS_SELECTOR, 'div[data-virtuoso-scroller="true"] > div > div')
        # sleep(5)
        booth_position = booths_div.find_element(By.CSS_SELECTOR, f'div[data-index="{id}"]')
        # sleep(5)
        return booth_position
    

    def scroll_a_bit(self, pixels : int = 100) -> None:
        """
        Scrolls DOWN booths in booths_div. Should be performed after closing of the scraped booth. Default scroll is 100px.
        """
        self._driver.execute_script(
            f"arguments[0].scrollTop = arguments[0].scrollTop + {pixels};", self._overlay_content_scrollable())



    def terminate(self) -> None:
        self._driver.quit()


    def _overlay_content_scrollable(self):
        sleep(5)
        shadow_host = self._driver.find_element(By.CSS_SELECTOR, 'div.expofp-floorplan > div')
        # sleep(5)
        self.shadow_root = self._driver.execute_script("return arguments[0].shadowRoot", shadow_host)
        # sleep(5)
        efp_layout = self.shadow_root.find_element(By.CSS_SELECTOR, 'div#efp-layout')
        # sleep(5)
        layout_fixed = efp_layout.find_element(By.CSS_SELECTOR, 'div.layout__fixed')
        # sleep(5)
        overlay = layout_fixed.find_element(By.CSS_SELECTOR, 'div.overlay')
        # sleep(5)
        overlay_content = overlay.find_element(By.CSS_SELECTOR, 'div#overlay-content')
        # sleep(5)
        return overlay_content.find_element(By.CSS_SELECTOR, 'div.overlay-content__scrollable')