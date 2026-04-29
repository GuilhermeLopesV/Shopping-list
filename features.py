def command_terminal(option, items):
    if option == 'I':
        value = input('Valor para adiciona a lista: ').strip().capitalize()
        if value:
            items.append(value)
        else:
            print('Não é possível adicionar valor vazio')

    elif option == 'A':
        if not items:
            print('Lista vazia')
            return

        for i, val in enumerate(items):
            print(i, val)

        indice_str = input('Escolha o índice para apagar: ')
        try:
            indice = int(indice_str)
            item_removed = items.pop(indice)
            print(f'Item "{item_removed}" foi removido da lista.')

        except ValueError:
            print('Por favor digite somente número int')
        except IndexError:
            print('Esse índice não existe')

    elif option == 'L':
        if not items:
            print('Lista vazia')

        for i, value in enumerate(items, start=1):
            print(i, value)

