from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from save_data import create_csv, add_to_csv

URL = 'https://ice25.expofp.com/'



def expand_shadow_element(driver, element):
    return driver.execute_script("return arguments[0].shadowRoot", element)


def open_url(URL: str):
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    return driver


def calculate_the_count_of_booths(driver):
    # 1. Получаем хост Shadow DOM
    shadow_host = driver.find_element(By.CSS_SELECTOR, 'div.expofp-floorplan > div')
    # 2. Получаем Shadow Root
    shadow_root = expand_shadow_element(driver, shadow_host)

    # 3. Получаем внутреннюю структуру
    efp_layout = shadow_root.find_element(By.CSS_SELECTOR, 'div#efp-layout')
    layout_fixed = efp_layout.find_element(By.CSS_SELECTOR, 'div.layout__fixed')
    overlay = layout_fixed.find_element(By.CSS_SELECTOR, 'div.overlay')
    overlay_content = overlay.find_element(By.CSS_SELECTOR, 'div#overlay-content')
    scrollable = overlay_content.find_element(By.CSS_SELECTOR, 'div.overlay-content__scrollable')
    virtual_scroll = scrollable.find_element(By.CSS_SELECTOR, 'div[style="height: 100%; cursor: pointer; resize: both; min-height: 100px;"]')
    virtuozo = virtual_scroll.find_element(By.CSS_SELECTOR, 'div[data-virtuoso-scroller="true"] > div > div')

    # 4. Получаем все элементы в списке (или часть, если список не подгрузился полностью)
    items = virtuozo.find_elements(By.CSS_SELECTOR, 'div[data-index]')
    
    return len(items)


def get_booth_by_id(driver, id=0):
    # 1. Получаем хост Shadow DOM
    shadow_host = driver.find_element(By.CSS_SELECTOR, 'div.expofp-floorplan > div')
    # 2. Получаем Shadow Root
    shadow_root = expand_shadow_element(driver, shadow_host)

    # 3. Получаем внутреннюю структуру
    efp_layout = shadow_root.find_element(By.CSS_SELECTOR, 'div#efp-layout')
    layout_fixed = efp_layout.find_element(By.CSS_SELECTOR, 'div.layout__fixed')
    overlay = layout_fixed.find_element(By.CSS_SELECTOR, 'div.overlay')
    overlay_content = overlay.find_element(By.CSS_SELECTOR, 'div#overlay-content')
    scrollable = overlay_content.find_element(By.CSS_SELECTOR, 'div.overlay-content__scrollable')
    virtual_scroll = scrollable.find_element(By.CSS_SELECTOR, 'div[style="height: 100%; cursor: pointer; resize: both; min-height: 100px;"]')
    virtuozo = virtual_scroll.find_element(By.CSS_SELECTOR, 'div[data-virtuoso-scroller="true"] > div > div')

    # 4. Получаем все элементы в списке (или часть, если список не подгрузился полностью)
    elements = virtuozo.find_elements(By.CSS_SELECTOR, 'div[data-index="{}"]'.format(id))
    if not elements:
        return None
    return elements[0]


def close_booth(driver):
    # 1. Получаем хост Shadow DOM
    shadow_host = driver.find_element(By.CSS_SELECTOR, 'div.expofp-floorplan > div')
    # 2. Получаем Shadow Root
    shadow_root = expand_shadow_element(driver, shadow_host)

    # 3. Получаем внутреннюю структуру
    efp_layout = shadow_root.find_element(By.CSS_SELECTOR, 'div#efp-layout')
    layout_fixed = efp_layout.find_element(By.CSS_SELECTOR, 'div.layout__fixed')
    overlay = layout_fixed.find_element(By.CSS_SELECTOR, 'div.overlay')
    overlay_content = overlay.find_element(By.CSS_SELECTOR, 'div#overlay-content')
    overlay_bar = overlay_content.find_element(By.CSS_SELECTOR, 'div.overlay-bar')
    overlay_bar_close = overlay_bar.find_element(By.CSS_SELECTOR, 'div.overlay-bar__close')
    close_button = overlay_bar_close.find_element(By.CSS_SELECTOR, 'button')
    close_button.click()  # Закрыть оверлей


def scroll_a_bit(driver):
    # 1. Получаем хост Shadow DOM
    shadow_host = driver.find_element(By.CSS_SELECTOR, 'div.expofp-floorplan > div')
    # 2. Получаем Shadow Root
    shadow_root = expand_shadow_element(driver, shadow_host)

    # 3. Получаем внутреннюю структуру
    efp_layout = shadow_root.find_element(By.CSS_SELECTOR, 'div#efp-layout')
    layout_fixed = efp_layout.find_element(By.CSS_SELECTOR, 'div.layout__fixed')
    overlay = layout_fixed.find_element(By.CSS_SELECTOR, 'div.overlay')
    overlay_content = overlay.find_element(By.CSS_SELECTOR, 'div#overlay-content')
    scrollable = overlay_content.find_element(By.CSS_SELECTOR, 'div.overlay-content__scrollable')
    # print(scrollable)
    # 1. Получаем хост Shadow 
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 100;", scrollable)


def get_company_name(driver):
        # 1. Получаем хост Shadow DOM
    shadow_host = driver.find_element(By.CSS_SELECTOR, 'div.expofp-floorplan > div')
    # 2. Получаем Shadow Root
    shadow_root = expand_shadow_element(driver, shadow_host)

    # 3. Получаем внутреннюю структуру
    efp_layout = shadow_root.find_element(By.CSS_SELECTOR, 'div#efp-layout')
    layout_fixed = efp_layout.find_element(By.CSS_SELECTOR, 'div.layout__fixed')
    overlay = layout_fixed.find_element(By.CSS_SELECTOR, 'div.overlay')
    overlay_content = overlay.find_element(By.CSS_SELECTOR, 'div#overlay-content')
    overlay_bar = overlay_content.find_element(By.CSS_SELECTOR, 'div.overlay-bar')
    company_name = overlay_bar.find_element(By.CSS_SELECTOR, 'div.overlay-bar__slot').text
    return company_name


def info_company_block(driver):
    # 1. Получаем хост Shadow DOM
    shadow_host = driver.find_element(By.CSS_SELECTOR, 'div.expofp-floorplan > div')
    # 2. Получаем Shadow Root
    shadow_root = expand_shadow_element(driver, shadow_host)

    # 3. Получаем внутреннюю структуру
    efp_layout = shadow_root.find_element(By.CSS_SELECTOR, 'div#efp-layout')
    layout_fixed = efp_layout.find_element(By.CSS_SELECTOR, 'div.layout__fixed')
    overlay = layout_fixed.find_element(By.CSS_SELECTOR, 'div.overlay')
    overlay_content = overlay.find_element(By.CSS_SELECTOR, 'div#overlay-content')
    overlay_content_scrollable = overlay_content.find_element(By.CSS_SELECTOR, 'div.overlay-content__scrollable')
    exhibitor_details = overlay_content_scrollable.find_elements(By.CSS_SELECTOR, 'div.exhibitor__details')
    if exhibitor_details:
        return exhibitor_details[0]
    else:
        return None


def get_company_description(driver):
    exhibitor_details = info_company_block(driver)
    if not exhibitor_details:
        return ''
    exibitor_description = exhibitor_details.find_elements(By.CSS_SELECTOR, 'div.exhibitor-description')
    if exibitor_description:
        return exibitor_description[0].text
    return ''


def meta_company_block(driver):
    exhibitor_details = info_company_block(driver)
    if not exhibitor_details:
        return ''
    exibitor_meta = exhibitor_details.find_elements(By.CSS_SELECTOR, 'div.exhibitor-meta')
    if exibitor_meta:
        return exibitor_meta[0]
    return None


def get_company_address(driver):
    if meta_company_block(driver):
        exibitor_meta_items = meta_company_block(driver).find_elements(By.CSS_SELECTOR, 'div.exhibitor-meta__item')
        if len(exibitor_meta_items) > 0:
            return exibitor_meta_items[0].text
    return ''


def get_company_phone(driver):
    if meta_company_block(driver):
        exibitor_meta_items = meta_company_block(driver).find_elements(By.CSS_SELECTOR, 'div.exhibitor-meta__item')
        if len(exibitor_meta_items) > 1:
            return exibitor_meta_items[1].text
    return ''


def get_company_website(driver):
    if meta_company_block(driver):
        exibitor_meta_items = meta_company_block(driver).find_elements(By.CSS_SELECTOR, 'div.exhibitor-meta__item')
        if len(exibitor_meta_items) > 2:
            return exibitor_meta_items[2].text
    return ''


def get_company_mail(driver):
    if meta_company_block(driver):
        exibitor_meta_items = meta_company_block(driver).find_elements(By.CSS_SELECTOR, 'div.exhibitor-meta__item')
        if len(exibitor_meta_items) > 3:
            return exibitor_meta_items[3].text
    return ''


def main():
    driver = open_url(URL)
    time.sleep(10)  # Дай странице загрузиться (если надо — увеличь)

    create_csv()

    for i in range(0, 16):  # Измените диапазон, если нужно больше или меньше
        print(f'Processing booth with ID: {i}')

        booth = get_booth_by_id(driver, i)
        
        booth.click()  # Кликаем по первому элементу
        
        time.sleep(5)  # Дай оверлею время на загрузку

        # Получаем данные компании из оверлея

        company_data = {
            'id': i,
            'name': get_company_name(driver),
            'description': get_company_description(driver),
            'address': get_company_address(driver),
            'phone': get_company_phone(driver),
            'website': get_company_website(driver),
            'mail': get_company_mail(driver)
        }

        close_booth(driver)  # Закрываем оверлей

        time.sleep(1)

        scroll_a_bit(driver)

        time.sleep(5)  # Дай оверлею время на загрузку

        print(f'Company data for booth {i}: {company_data}')


        # Записываем данные в CSV
        add_to_csv(company_data.values())

    driver.quit()




if __name__ == "__main__":
    main()
