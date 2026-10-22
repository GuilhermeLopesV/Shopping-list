import unittest
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout

from features import (
    add_item,
    remove_item,
    edit_quantity,
    toggle_purchased,
    list_items,
    command_terminal
)


class TestShoppingList(unittest.TestCase):

    def test_add_item(self):
        items = []

        with patch('builtins.input', side_effect=['arroz', '2']):
            result = add_item(items)

        self.assertTrue(result)
        self.assertEqual(
            items,
            [{'nome': 'Arroz', 'quantidade': 2, 'comprado': False}]
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
            {'nome': 'Arroz', 'quantidade': 2, 'comprado': False},
            {'nome': 'Feijão', 'quantidade': 1, 'comprado': False},
            {'nome': 'Leite', 'quantidade': 3, 'comprado': True}
        ]

        with patch('builtins.input', return_value='2'):
            result = remove_item(items)

        self.assertTrue(result)
        self.assertEqual(
            items,
            [
                {'nome': 'Arroz', 'quantidade': 2, 'comprado': False},
                {'nome': 'Leite', 'quantidade': 3, 'comprado': True}
            ]
        )

    def test_remove_invalid_index(self):
        items = [
            {'nome': 'Arroz', 'quantidade': 2, 'comprado': False},
            {'nome': 'Feijão', 'quantidade': 1, 'comprado': False}
        ]

        with patch('builtins.input', return_value='10'):
            result = remove_item(items)

        self.assertFalse(result)
        self.assertEqual(len(items), 2)

    def test_list_items(self):
        items = [
            {'nome': 'Arroz', 'quantidade': 2, 'comprado': False},
            {'nome': 'Feijão', 'quantidade': 1, 'comprado': True}
        ]

        output = StringIO()

        with redirect_stdout(output):
            list_items(items)

        self.assertIn('1. Arroz', output.getvalue())
        self.assertIn('Quantidade: 2', output.getvalue())
        self.assertIn('Pendente', output.getvalue())
        self.assertIn('2. Feijão', output.getvalue())
        self.assertIn('Quantidade: 1', output.getvalue())
        self.assertIn('Comprado', output.getvalue())

    def test_invalid_option(self):
        items = [
            {'nome': 'Arroz', 'quantidade': 1, 'comprado': False}
        ]

        result = command_terminal('X', items)

        self.assertFalse(result)
        self.assertEqual(len(items), 1)

    def test_edit_quantity(self):
        items = [
            {'nome': 'Arroz', 'quantidade': 2, 'comprado': False}
        ]

        with patch('builtins.input', side_effect=['1', '5']):
            result = edit_quantity(items)

        self.assertTrue(result)
        self.assertEqual(items[0]['quantidade'], 5)

    def test_edit_quantity_invalid_index(self):
        items = [
            {'nome': 'Arroz', 'quantidade': 2, 'comprado': False}
        ]

        with patch('builtins.input', return_value='10'):
            result = edit_quantity(items)

        self.assertFalse(result)
        self.assertEqual(items[0]['quantidade'], 2)

    def test_edit_quantity_invalid_value(self):
        items = [
            {'nome': 'Arroz', 'quantidade': 2, 'comprado': False}
        ]

        with patch('builtins.input', side_effect=['1', '0']):
            result = edit_quantity(items)

        self.assertFalse(result)
        self.assertEqual(items[0]['quantidade'], 2)

    def test_edit_quantity_empty_list(self):
        items = []

        result = edit_quantity(items)

        self.assertFalse(result)
        self.assertEqual(items, [])

    def test_toggle_purchased(self):
        items = [
            {'nome': 'Arroz', 'quantidade': 2, 'comprado': False}
        ]

        with patch('builtins.input', return_value='1'):
            result = toggle_purchased(items)

        self.assertTrue(result)
        self.assertTrue(items[0]['comprado'])

    def test_toggle_purchased_back_to_pending(self):
        items = [
            {'nome': 'Arroz', 'quantidade': 2, 'comprado': True}
        ]

        with patch('builtins.input', return_value='1'):
            result = toggle_purchased(items)

        self.assertTrue(result)
        self.assertFalse(items[0]['comprado'])

    def test_toggle_purchased_invalid_index(self):
        items = [
            {'nome': 'Arroz', 'quantidade': 2, 'comprado': False}
        ]

        with patch('builtins.input', return_value='10'):
            result = toggle_purchased(items)

        self.assertFalse(result)
        self.assertFalse(items[0]['comprado'])

    def test_toggle_purchased_empty_list(self):
        items = []

        result = toggle_purchased(items)

        self.assertFalse(result)
        self.assertEqual(items, [])


if __name__ == '__main__':
    unittest.main()