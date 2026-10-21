import json
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

    history = data.get('history', [])

    if not isinstance(history, list):
        print('Formato de dados inválido. Iniciando uma lista vazia.')
        return []

    return [item for item in history if isinstance(item, str)]
