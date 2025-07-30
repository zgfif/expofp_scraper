import time
from save_data import create_csv, add_to_csv
from booth_scraper import BoothScraper


# URL of the ExpoFP page
URL = 'https://ice25.expofp.com/'


# Number of booths to process
# Adjust this value based on the actual number of booths available
BOOTH_COUNT = 5


def main() -> None:
    scraper = BoothScraper(URL)
    scraper.open_url()

    time.sleep(10)  # Дай странице загрузиться (если надо — увеличь)

    create_csv()

    for i in range(0, BOOTH_COUNT):  # Измените диапазон, если нужно больше или меньше
        print(f'Processing booth with ID: {i}')
        scraper.find_shadow_root()
        
        scraper.find_booths_div()
        
        scraper.get_booth_by_id(i)

        scraper.booth.click()

        time.sleep(5)

        company_data = scraper.extract_company_details()
        
        data = {'id': i, **company_data}
        
        scraper.get_close_button()        

        time.sleep(5)  # Дай оверлею время на загрузку

        print(f'Company data for booth {i}: {data}')


        # Записываем данные в CSV
        add_to_csv(data.values())

        scraper.close_button.click()

        scraper.scroll_a_bit()

    scraper.terminate()

    print(f'Scraping {BOOTH_COUNT} booths is finished!')




if __name__ == "__main__":
    main()
