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
        'quantidade': quantity,
        'comprado': False
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



def edit_quantity(items):
    if not items:
        print('Sua lista está vazia.')
        return False

    list_items(items)

    try:
        index = int(input('Digite o número do produto: '))

        if index < 1 or index > len(items):
            print('Esse número não corresponde a um produto da lista.')
            return False

        item = items[index - 1]

        quantity = int(input('Digite a nova quantidade: '))

        if quantity <= 0:
            print('A quantidade deve ser maior que zero.')
            return False

        old_quantity = item['quantidade']
        item['quantidade'] = quantity

        print(
            f'Quantidade de "{item["nome"]}" atualizada '
            f'de {old_quantity} para {quantity}.'
        )

        return True

    except ValueError:
        print('Digite um número inteiro válido.')
        return False


def toggle_purchased(items):
    if not items:
        print('Sua lista está vazia.')
        return False

    list_items(items)

    try:
        index = int(input('Digite o número do produto: '))

        if index < 1 or index > len(items):
            print('Esse número não corresponde a um produto da lista.')
            return False

        item = items[index - 1]
        item['comprado'] = not item['comprado']

        status = 'comprado' if item['comprado'] else 'pendente'

        print(f'"{item["nome"]}" marcado como {status}.')

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
        status = 'Comprado' if item['comprado'] else 'Pendente'

        print(
            f'{index}. {item["nome"]} '
            f'- Quantidade: {item["quantidade"]} '
            f'- {status}'
        )

    print('-' * 30)


def command_terminal(option, items):
    if option == 'I':
        return add_item(items)

    elif option == 'A':
        return remove_item(items)

    elif option == 'Q':
        return edit_quantity(items)

    elif option == 'M':
        return toggle_purchased(items)

    elif option == 'L':
        list_items(items)

    return False

