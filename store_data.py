import csv

def create_csv(filename='output.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Записываем заголовки столбцов
        writer.writerow(['id', 'name', 'description', 'address', 'phone', 'website', 'mail'])


def add_to_csv(data: list, filename='output.csv'):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)
