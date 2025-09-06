shopping_list = []

while True:
    print('-' * 30)
    print('Selecione uma opção')
    option = input('[I]nserir [A]pagar [L]istar [E]ncerrar: ').upper()

    if option == 'I':
        value = input('Valor para adiciona a lista: ').strip().capitalize()
        if value:
            shopping_list.append(value)
        else:
            print('Não é possível adicionar valor vazio')

    elif option == 'A':
        if not shopping_list:
            print('Lista vazia')
            continue

        for i, val in enumerate(shopping_list):
            print(i, val)

        indice_str = input('Escolha o índice para apagar: ')
        try:
            indice = int(indice_str)
            item_removed = shopping_list.pop(indice)
            print(f'Item "{item_removed}" foi removido da lista.')

        except ValueError:
            print('Por favor digite somente número int')
        except IndexError:
            print('Esse índice não existe')

    elif option == 'L':
        if not shopping_list:
            print('Lista vazia')

        for i, value in enumerate(shopping_list):
            print(i, value)

    elif option == 'E':
        print('Programa finalizado')
        break