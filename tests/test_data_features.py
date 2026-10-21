import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from package_data.data_features import save_data, load_data


class TestShoppingListData(unittest.TestCase):

    def test_save_data(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / 'history.json'

            with patch('package_data.data_features.FILE_PATH', test_file):
                result = save_data(['Arroz', 'Feijão'])

            self.assertTrue(result)
            self.assertTrue(test_file.exists())

            with open(test_file, 'r', encoding='utf-8') as file:
                data = json.load(file)

            self.assertEqual(data['history'], ['Arroz', 'Feijão'])

    def test_load_data(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / 'history.json'

            with open(test_file, 'w', encoding='utf-8') as file:
                json.dump(
                    {'history': ['Arroz', 'Feijão']},
                    file
                )

            with patch('package_data.data_features.FILE_PATH', test_file):
                result = load_data()

            self.assertEqual(result, ['Arroz', 'Feijão'])

    def test_load_missing_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / 'missing.json'

            with patch('package_data.data_features.FILE_PATH', test_file):
                result = load_data()

            self.assertEqual(result, [])

    def test_load_invalid_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / 'history.json'
            test_file.write_text('{json inválido', encoding='utf-8')

            with patch('package_data.data_features.FILE_PATH', test_file):
                result = load_data()

            self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
