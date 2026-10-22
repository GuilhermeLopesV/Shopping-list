import unittest
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout

from features import add_item, remove_item, edit_quantity, list_items, command_terminal


class TestShoppingList(unittest.TestCase):

    def test_add_item(self):
        items = []

        with patch('builtins.input', side_effect=['arroz', '2']):
            result = add_item(items)

        self.assertTrue(result)
        self.assertEqual(
            items,
            [{'nome': 'Arroz', 'quantidade': 2}]
        )

    def test_add_empty_item(self):
        items = []

        with patch('builtins.input', return_value='   '):
            result = add_item(items)

        self.assertFalse(result)
        self.assertEqual(items, [])

    def test_add_invalid_quantity(self):
        items = []

        with patch('builtins.input', side_effect=['Arroz', '0']):
            result = add_item(items)

        self.assertFalse(result)
        self.assertEqual(items, [])

    def test_add_non_numeric_quantity(self):
        items = []

        with patch('builtins.input', side_effect=['Arroz', 'abc']):
            result = add_item(items)

        self.assertFalse(result)
        self.assertEqual(items, [])

    def test_remove_item(self):
        items = [
            {'nome': 'Arroz', 'quantidade': 2},
            {'nome': 'Feijão', 'quantidade': 1},
            {'nome': 'Leite', 'quantidade': 3}
        ]

        with patch('builtins.input', return_value='2'):
            result = remove_item(items)

        self.assertTrue(result)
        self.assertEqual(
            items,
            [
                {'nome': 'Arroz', 'quantidade': 2},
                {'nome': 'Leite', 'quantidade': 3}
            ]
        )

    def test_remove_invalid_index(self):
        items = [
            {'nome': 'Arroz', 'quantidade': 2},
            {'nome': 'Feijão', 'quantidade': 1}
        ]

        with patch('builtins.input', return_value='10'):
            result = remove_item(items)

        self.assertFalse(result)
        self.assertEqual(len(items), 2)

    def test_list_items(self):
        items = [
            {'nome': 'Arroz', 'quantidade': 2},
            {'nome': 'Feijão', 'quantidade': 1}
        ]

        output = StringIO()

        with redirect_stdout(output):
            list_items(items)

        self.assertIn('1. Arroz', output.getvalue())
        self.assertIn('Quantidade: 2', output.getvalue())
        self.assertIn('2. Feijão', output.getvalue())
        self.assertIn('Quantidade: 1', output.getvalue())

    def test_invalid_option(self):
        items = [{'nome': 'Arroz', 'quantidade': 1}]

        result = command_terminal('X', items)

        self.assertFalse(result)
        self.assertEqual(len(items), 1)

    def test_edit_quantity(self):
        items = [{'nome': 'Arroz', 'quantidade': 2}]

        with patch('builtins.input', side_effect=['1', '5']):
            result = edit_quantity(items)

        self.assertTrue(result)
        self.assertEqual(items[0]['quantidade'], 5)

    def test_edit_quantity_invalid_index(self):
        items = [{'nome': 'Arroz', 'quantidade': 2}]

        with patch('builtins.input', return_value='10'):
            result = edit_quantity(items)

        self.assertFalse(result)
        self.assertEqual(items[0]['quantidade'], 2)

    def test_edit_quantity_invalid_value(self):
        items = [{'nome': 'Arroz', 'quantidade': 2}]

        with patch('builtins.input', side_effect=['1', '0']):
            result = edit_quantity(items)

        self.assertFalse(result)
        self.assertEqual(items[0]['quantidade'], 2)

    def test_edit_quantity_empty_list(self):
        items = []

        result = edit_quantity(items)

        self.assertFalse(result)
        self.assertEqual(items, [])


if __name__ == '__main__':
    unittest.main()
