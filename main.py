from features import command_terminal
from package_data.data_features import load_data, save_data


def shopping_list_manager():
    shopping_list = list(load_data())

    while True:
        print('-' * 30)
        print('Selecione uma opção')
        option = input('[I]nserir [A]pagar [L]istar [E]ncerrar: ').upper()

        command_terminal(option, shopping_list)

        save_data(shopping_list)

        if option == 'E':
            print('Programa finalizado')
            break

shopping_list_manager()