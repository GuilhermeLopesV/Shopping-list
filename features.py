def add_item(items):
    value = input('Produto para adicionar: ').strip()

    if not value:
        print('Não é possível adicionar um produto vazio.')
        return False

    items.append(value.capitalize())
    print(f'Produto "{value.capitalize()}" adicionado com sucesso.')

    return True


def remove_item(items):
    if not items:
        print('Sua lista está vazia.')
        return False

    list_items(items)

    try:
        index = int(input('Digite o número do produto para remover: '))
        item_removed = items.pop(index - 1)

        print(f'Produto "{item_removed}" removido com sucesso.')
        return True

    except ValueError:
        print('Digite um número inteiro válido.')
    except IndexError:
        print('Esse número não corresponde a um produto da lista.')

    return False


def list_items(items):
    if not items:
        print('Sua lista está vazia.')
        return

    print('\n--- SUA LISTA DE COMPRAS ---')

    for index, item in enumerate(items, start=1):
        print(f'{index}. {item}')

    print('-' * 30)


def command_terminal(option, items):
    if option == 'I':
        return add_item(items)

    elif option == 'A':
        return remove_item(items)

    elif option == 'L':
        list_items(items)

    return False
