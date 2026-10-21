import unittest
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout

from features import add_item, remove_item, list_items, command_terminal


class TestShoppingList(unittest.TestCase):

    def test_add_item(self):
        items = []

        with patch('builtins.input', return_value='arroz'):
            result = add_item(items)

        self.assertTrue(result)
        self.assertEqual(items, ['Arroz'])

    def test_add_empty_item(self):
        items = []

        with patch('builtins.input', return_value='   '):
            result = add_item(items)

        self.assertFalse(result)
        self.assertEqual(items, [])

    def test_remove_item(self):
        items = ['Arroz', 'Feijão', 'Leite']

        with patch('builtins.input', return_value='2'):
            result = remove_item(items)

        self.assertTrue(result)
        self.assertEqual(items, ['Arroz', 'Leite'])

    def test_remove_invalid_index(self):
        items = ['Arroz', 'Feijão']

        with patch('builtins.input', return_value='10'):
            result = remove_item(items)

        self.assertFalse(result)
        self.assertEqual(items, ['Arroz', 'Feijão'])

    def test_list_items(self):
        items = ['Arroz', 'Feijão']
        output = StringIO()

        with redirect_stdout(output):
            list_items(items)

        self.assertIn('1. Arroz', output.getvalue())
        self.assertIn('2. Feijão', output.getvalue())

    def test_invalid_option(self):
        items = ['Arroz']

        result = command_terminal('X', items)

        self.assertFalse(result)
        self.assertEqual(items, ['Arroz'])


if __name__ == '__main__':
    unittest.main()
