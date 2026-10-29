from features import command_terminal
from package_data.data_features import load_data, save_data


def shopping_list_manager():
    shopping_list = load_data()

    while True:
        print('\n' + '-' * 30)
        print('       LISTA DE COMPRAS')
        print('-' * 30)
        print('[I] Inserir produto')
        print('[A] Apagar produto')
        print('[L] Listar produtos')
        print('[Q] Editar quantidade')
        print('[P] Editar preço de produto')
        print('[M] Marcar produto como comprado')
        print('[E] Encerrar programa')

        option = input('Escolha uma opção: ').strip().upper()

        if option == 'E':
            print('Programa finalizado.')
            break

        if option not in {'I', 'A', 'L', 'Q', 'M', 'P'}:
            print('Opção inválida. Tente novamente.')
            continue

        changed = command_terminal(option, shopping_list)

        if changed:
            save_data(shopping_list)


if __name__ == '__main__':
    shopping_list_manager()
