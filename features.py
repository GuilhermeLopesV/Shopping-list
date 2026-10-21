def add_item(items):
    name = input('Produto para adicionar: ').strip()

    if not name:
        print('Não é possível adicionar um produto vazio.')
        return False

    try:
        quantity = int(input('Quantidade do produto: '))

        if quantity <= 0:
            print('A quantidade deve ser maior que zero.')
            return False

    except ValueError:
        print('Digite uma quantidade inteira válida.')
        return False

    item = {
        'nome': name.capitalize(),
        'quantidade': quantity
    }

    items.append(item)

    print(
        f'Produto "{item["nome"]}" adicionado '
        f'com quantidade {quantity}.'
    )

    return True


def remove_item(items):
    if not items:
        print('Sua lista está vazia.')
        return False

    list_items(items)

    try:
        index = int(input('Digite o número do produto para remover: '))

        if index < 1 or index > len(items):
            print('Esse número não corresponde a um produto da lista.')
            return False

        item_removed = items.pop(index - 1)

        print(f'Produto "{item_removed["nome"]}" removido com sucesso.')
        return True

    except ValueError:
        print('Digite um número inteiro válido.')
        return False


def list_items(items):
    if not items:
        print('Sua lista está vazia.')
        return

    print('\n--- SUA LISTA DE COMPRAS ---')

    for index, item in enumerate(items, start=1):
        print(
            f'{index}. {item["nome"]} '
            f'- Quantidade: {item["quantidade"]}'
        )

    print('-' * 30)


def command_terminal(option, items):
    if option == 'I':
        return add_item(items)

    elif option == 'A':
        return remove_item(items)

    elif option == 'L':
        list_items(items)

    return False
