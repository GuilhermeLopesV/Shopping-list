import unittest
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout
from decimal import Decimal

from features import (
    add_item,
    remove_item,
    edit_quantity,
    edit_price,
    toggle_purchased,
    list_items,
    filter_items,
    command_terminal,
    calculate_total,
    calculate_pending_total,
)


class TestShoppingList(unittest.TestCase):

    def test_add_item(self):
        items = []

        with patch(
                'builtins.input',
                side_effect=['arroz', '2', '25,90']
        ):
            result = add_item(items)

        self.assertTrue(result)
        self.assertEqual(
            items,
            [{
                'nome': 'Arroz',
                'quantidade': 2,
                'comprado': False,
                'preco': '25.90'
            }]
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
            {
                'nome': 'Arroz',
                'quantidade': 2,
                'comprado': False,
                'preco': '25.90'
            },
            {
                'nome': 'Feijão',
                'quantidade': 3,
                'comprado': True,
                'preco': '8.50'
            }
        ]

        output = StringIO()

        with redirect_stdout(output):
            list_items(items)

        result = output.getvalue()

        self.assertIn('1. Arroz', result)
        self.assertIn('Quantidade: 2', result)
        self.assertIn('Preço unitário: R$ 25.90', result)
        self.assertIn('Subtotal: R$ 51.80', result)
        self.assertIn('Pendente', result)

        self.assertIn('2. Feijão', result)
        self.assertIn('Quantidade: 3', result)
        self.assertIn('Preço unitário: R$ 8.50', result)
        self.assertIn('Subtotal: R$ 25.50', result)
        self.assertIn('Comprado', result)


    def test_filter_all_items(self):
        items = [
            {
                'nome': 'Arroz',
                'quantidade': 2,
                'comprado': False,
                'preco': '10.00'
            },
            {
                'nome': 'Feijão',
                'quantidade': 1,
                'comprado': True,
                'preco': '8.50'
            }
        ]

        output = StringIO()

        with patch('builtins.input', return_value='T'):
            with redirect_stdout(output):
                filter_items(items)

        result = output.getvalue()

        self.assertIn('Arroz', result)
        self.assertIn('Feijão', result)

    def test_filter_pending_items(self):
        items = [
            {
                'nome': 'Arroz',
                'quantidade': 2,
                'comprado': False,
                'preco': '10.00'
            },
            {
                'nome': 'Feijão',
                'quantidade': 1,
                'comprado': True,
                'preco': '8.50'
            }
        ]

        output = StringIO()

        with patch('builtins.input', return_value='P'):
            with redirect_stdout(output):
                filter_items(items)

        result = output.getvalue()

        self.assertIn('Arroz', result)
        self.assertNotIn('Feijão', result)

    def test_filter_purchased_items(self):
        items = [
            {
                'nome': 'Arroz',
                'quantidade': 2,
                'comprado': False,
                'preco': '10.00'
            },
            {
                'nome': 'Feijão',
                'quantidade': 1,
                'comprado': True,
                'preco': '8.50'
            }
        ]

        output = StringIO()

        with patch('builtins.input', return_value='C'):
            with redirect_stdout(output):
                filter_items(items)

        result = output.getvalue()

        self.assertNotIn('Arroz', result)
        self.assertIn('Feijão', result)

    def test_filter_without_matching_items(self):
        items = [
            {
                'nome': 'Arroz',
                'quantidade': 2,
                'comprado': False,
                'preco': '10.00'
            }
        ]

        output = StringIO()

        with patch('builtins.input', return_value='C'):
            with redirect_stdout(output):
                filter_items(items)

        self.assertIn(
            'Nenhum produto encontrado para esse filtro.',
            output.getvalue()
        )

    def test_filter_invalid_option(self):
        items = [
            {
                'nome': 'Arroz',
                'quantidade': 2,
                'comprado': False,
                'preco': '10.00'
            }
        ]

        output = StringIO()

        with patch('builtins.input', return_value='X'):
            with redirect_stdout(output):
                filter_items(items)

        self.assertIn('Opção inválida.', output.getvalue())

    def test_filter_empty_list(self):
        items = []

        output = StringIO()

        with redirect_stdout(output):
            filter_items(items)

        self.assertIn('Sua lista está vazia.', output.getvalue())

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

    def test_edit_price(self):
        items = [
            {
                'nome': 'Arroz',
                'quantidade': 2,
                'comprado': False,
                'preco': '10.00'
            }
        ]

        with patch('builtins.input', side_effect=['1', '12,50']):
            result = edit_price(items)

        self.assertTrue(result)
        self.assertEqual(items[0]['preco'], '12.50')
        self.assertEqual(calculate_total(items), Decimal('25.00'))

    def test_edit_price_invalid_index(self):
        items = [
            {
                'nome': 'Arroz',
                'quantidade': 2,
                'comprado': False,
                'preco': '10.00'
            }
        ]

        with patch('builtins.input', return_value='10'):
            result = edit_price(items)

        self.assertFalse(result)
        self.assertEqual(items[0]['preco'], '10.00')

    def test_edit_price_invalid_value(self):
        items = [
            {
                'nome': 'Arroz',
                'quantidade': 2,
                'comprado': False,
                'preco': '10.00'
            }
        ]

        with patch('builtins.input', side_effect=['1', 'abc']):
            result = edit_price(items)

        self.assertFalse(result)
        self.assertEqual(items[0]['preco'], '10.00')

    def test_edit_price_more_than_two_decimal_places(self):
        items = [
            {
                'nome': 'Arroz',
                'quantidade': 2,
                'comprado': False,
                'preco': '10.00'
            }
        ]

        with patch('builtins.input', side_effect=['1', '12.555']):
            result = edit_price(items)

        self.assertFalse(result)
        self.assertEqual(items[0]['preco'], '10.00')

    def test_edit_price_empty_list(self):
        items = []

        result = edit_price(items)

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

    def test_calculate_total(self):
        items = [
            {
                'nome': 'Arroz',
                'quantidade': 2,
                'comprado': False,
                'preco': '25.90'
            },
            {
                'nome': 'Feijão',
                'quantidade': 3,
                'comprado': True,
                'preco': '8.50'
            }
        ]

        result = calculate_total(items)

        self.assertEqual(result, Decimal('77.30'))

    def test_calculate_total_empty_list(self):
        result = calculate_total([])

        self.assertEqual(result, Decimal('0.00'))

    def test_calculate_pending_total(self):
        items = [
            {
                'nome': 'Arroz',
                'quantidade': 2,
                'comprado': False,
                'preco': '10.00'
            },
            {
                'nome': 'Feijão',
                'quantidade': 1,
                'comprado': True,
                'preco': '8.50'
            },
            {
                'nome': 'Leite',
                'quantidade': 3,
                'comprado': False,
                'preco': '5.00'
            }
        ]

        result = calculate_pending_total(items)

        self.assertEqual(result, Decimal('35.00'))

    def test_calculate_pending_total_all_purchased(self):
        items = [
            {
                'nome': 'Arroz',
                'quantidade': 2,
                'comprado': True,
                'preco': '10.00'
            },
            {
                'nome': 'Feijão',
                'quantidade': 1,
                'comprado': True,
                'preco': '8.50'
            }
        ]

        result = calculate_pending_total(items)

        self.assertEqual(result, Decimal('0.00'))

    def test_calculate_pending_total_empty_list(self):
        result = calculate_pending_total([])

        self.assertEqual(result, Decimal('0.00'))

    def test_calculate_pending_total_all_pending(self):
        items = [
            {
                'nome': 'Arroz',
                'quantidade': 2,
                'comprado': False,
                'preco': '10.00'
            },
            {
                'nome': 'Feijão',
                'quantidade': 1,
                'comprado': False,
                'preco': '8.50'
            }
        ]

        result = calculate_pending_total(items)

        self.assertEqual(result, Decimal('28.50'))

if __name__ == '__main__':
    unittest.main()