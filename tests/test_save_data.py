import unittest
import os
from save_data import create_csv, add_to_csv


class TestStoreData(unittest.TestCase):
    def setUp(self):
        for filename in ['output.csv', 'custom_exhibitors.csv', 'test_output.csv']:
            if os.path.exists(filename):
                os.remove(filename)


    def test_create_file_with_default_name_and_fields(self):
        # Test if the CSV file is created successfully
        create_csv()
        self.assertFalse(os.path.exists('exhibitors.csv'))
        self.assertTrue(os.path.exists('output.csv'))

        with open('output.csv', 'r', encoding='utf-8') as file:
            header = file.readline().strip()
            self.assertIn('id,name,description,address,phone,website,email', header)

    
    def test_create_file_with_custom_name(self):
        # Test if the CSV file is created with a custom name
        create_csv('custom_exhibitors.csv')
        
        self.assertTrue(os.path.exists('custom_exhibitors.csv'))

        with open('custom_exhibitors.csv', 'r', encoding='utf-8') as file:
            header = file.readline().strip()
            self.assertIn('id,name,description,address,phone,website,email', header)


    def test_add_to_csv(self):
        # Test if data is added to the CSV file correctly
        create_csv('test_output.csv')
        data = ['1', 
                'Test Company', 
                'This is a test description', 
                '123 Test St', '123-456-7890', 
                'http://test.com', 
                'mail@example.com'
        ]

        add_to_csv(data, 'test_output.csv')

        with open('test_output.csv', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            first_line = lines[0].strip().split(',')
            last_line = lines[-1].strip().split(',')

            self.assertEqual(first_line, ['id', 'name', 'description', 'address', 'phone', 'website', 'email'])
            self.assertEqual(last_line, data)
            self.assertEqual(len(lines), 2)
   
    
    def tearDown(self):
        # Clean up the created files after tests
        for filename in ['output.csv', 'custom_exhibitors.csv', 'test_output.csv']:
            if os.path.exists(filename):
                os.remove(filename)


if __name__ == '__main__':
    unittest.main()