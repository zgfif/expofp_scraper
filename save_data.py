import csv


def create_csv(filename='output.csv') -> None:
    """
    Creates a new CSV file with predefined column headers.
    """
    table_column_names = ('id', 'name', 'description', 'address', 'phone', 'website', 'email')
    
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write column headers
            writer.writerow(table_column_names)
    except IOError as e:
        print(f"Error creating file {filename}: {e}")


def add_to_csv(data: list[str], filename='output.csv') -> None:
    """
    Appends a row of data to the CSV file.
    """
    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(data)
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")
