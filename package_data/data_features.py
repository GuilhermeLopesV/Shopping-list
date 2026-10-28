import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR / 'history.json'


def save_data(items):
    data = {
        'history': items
    }

    try:
        with open(FILE_PATH, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        return True

    except OSError:
        print('Erro ao salvar os dados da lista.')
        return False


def load_data():
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print('O arquivo de dados está inválido. Iniciando uma lista vazia.')
        return []

    except OSError:
        print('Erro ao ler os dados. Iniciando uma lista vazia.')
        return []

    history = data.get('history', []) if isinstance(data, dict) else None

    if not isinstance(history, list):
        print('Formato de dados inválido. Iniciando uma lista vazia.')
        return []

    items = []

    for item in history:
        if isinstance(item, str):
            name = item.strip()

            if name:
                items.append({
                    'nome': name,
                    'quantidade': 1,
                    'comprado': False,
                    'preco': '0.00'
                })

        elif isinstance(item, dict):
            name = item.get('nome')
            quantity = item.get('quantidade')
            purchased = item.get('comprado', False)
            price = item.get('preco', '0.00')

            if isinstance(price, (int, float)) and not isinstance(price, bool):
                price = str(price)

            try:
                valid_price = (
                    isinstance(price, str)
                    and price.strip() != ''
                    and Decimal(price).is_finite()
                    and Decimal(price) >= 0
                    and Decimal(price).as_tuple().exponent >= -2
                )
            except InvalidOperation:
                valid_price = False

            if (
                isinstance(name, str)
                and name.strip()
                and isinstance(quantity, int)
                and not isinstance(quantity, bool)
                and quantity > 0
                and isinstance(purchased, bool)
                and valid_price
            ):
                items.append({
                    'nome': name.strip(),
                    'quantidade': quantity,
                    'comprado': purchased,
                    'preco': str(Decimal(price))
                })

    return items