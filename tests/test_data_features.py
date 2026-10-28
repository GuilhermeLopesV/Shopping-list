import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from package_data.data_features import save_data, load_data


class TestShoppingListData(unittest.TestCase):

    def test_save_data(self):
        items = [
            {
                'nome': 'Arroz',
                'quantidade': 2,
                'comprado': False,
                'preco': '5.70'
            },
            {
                'nome': 'Feijão',
                'quantidade': 1,
                'comprado': True,
                'preco': '8.50'
            }
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / 'history.json'

            with patch('package_data.data_features.FILE_PATH', test_file):
                result = save_data(items)

            self.assertTrue(result)
            self.assertTrue(test_file.exists())

            with open(test_file, 'r', encoding='utf-8') as file:
                data = json.load(file)

            self.assertEqual(data['history'], items)

    def test_load_data(self):
        expected = [
            {
                'nome': 'Arroz',
                'quantidade': 2,
                'comprado': False,
                'preco': '0.00'
            },
            {
                'nome': 'Feijão',
                'quantidade': 1,
                'comprado': True,
                'preco': '0.00'
            }
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / 'history.json'

            with open(test_file, 'w', encoding='utf-8') as file:
                json.dump({'history': expected}, file)

            with patch('package_data.data_features.FILE_PATH', test_file):
                result = load_data()

            self.assertEqual(result, expected)

    def test_load_legacy_data(self):
        legacy_items = ['Arroz', 'Feijão']

        expected = [
            {
                'nome': 'Arroz',
                'quantidade': 1,
                'comprado': False,
                'preco': '0.00'
            },
            {
                'nome': 'Feijão',
                'quantidade': 1,
                'comprado': False,
                'preco': '0.00'
            }
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / 'history.json'

            with open(test_file, 'w', encoding='utf-8') as file:
                json.dump({'history': legacy_items}, file)

            with patch('package_data.data_features.FILE_PATH', test_file):
                result = load_data()

            self.assertEqual(result, expected)

    def test_load_data_without_purchased_field(self):
        old_items = [
            {'nome': 'Arroz', 'quantidade': 2},
            {'nome': 'Feijão', 'quantidade': 1}
        ]

        expected = [
            {
                'nome': 'Arroz',
                'quantidade': 2,
                'comprado': False,
                'preco': '0.00'
            },
            {
                'nome': 'Feijão',
                'quantidade': 1,
                'comprado': False,
                'preco': '0.00'
            }
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / 'history.json'

            with open(test_file, 'w', encoding='utf-8') as file:
                json.dump({'history': old_items}, file)

            with patch('package_data.data_features.FILE_PATH', test_file):
                result = load_data()

            self.assertEqual(result, expected)

    def test_load_missing_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / 'missing.json'

            with patch('package_data.data_features.FILE_PATH', test_file):
                result = load_data()

            self.assertEqual(result, [])

    def test_load_invalid_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / 'history.json'
            test_file.write_text(
                '{json inválido',
                encoding='utf-8'
            )

            with patch('package_data.data_features.FILE_PATH', test_file):
                result = load_data()

            self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()