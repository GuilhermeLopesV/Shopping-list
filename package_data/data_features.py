import json
import os

BASE_DIR = os.path.dirname(__file__)
FILE_PATH = os.path.join(BASE_DIR, "history.json")


def save_data(results):
    data = {
        'history': results,
    }
    with open(FILE_PATH, "w") as arquivo:
        json.dump(data, arquivo, indent=4)


def load_data():
    try:
        with open(FILE_PATH, "r") as arquivo:
            data = json.load(arquivo)
        return data.get('history', [])
    except FileNotFoundError:
        return []