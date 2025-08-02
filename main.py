from save_data import create_csv, add_to_csv
from booth_menu import BoothMenu
from booth_page import BoothPage


BOOTH_COUNT= 171


def main():
    bm = BoothMenu()

    create_csv()

    for i in range(0, BOOTH_COUNT):
        print(f'Processing {i} booth...')
        
        position = bm.find_booth_position(i)
        
        bp = BoothPage(position, bm._driver)
        
        details = {
            'id': i,
            'name': bp.extract_name(),
            'description': bp.extract_description(),
            **bp.extract_additional_details()
        }

        print(details)
        
        add_to_csv(details.values())
        
        bp.close()

        bm.scroll_a_bit()

    bm.terminate()

    print(f'Parsing has been finished! Parsed {BOOTH_COUNT} booths.')


if __name__ == '__main__':
    main()
