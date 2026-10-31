from decimal import Decimal, InvalidOperation


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

    try:
        price_input = input('Preço unitário do produto (R$): ')
        price_input = price_input.strip().replace(',', '.')

        price = Decimal(price_input)

        if not price.is_finite() or price < 0:
            print('O preço deve ser um valor válido e não negativo.')
            return False

        if price.as_tuple().exponent < -2:
            print('O preço deve ter no máximo duas casas decimais.')
            return False

    except InvalidOperation:
        print('Digite um preço válido.')
        return False

    item = {
        'nome': name.capitalize(),
        'quantidade': quantity,
        'comprado': False,
        'preco': str(price)
    }

    items.append(item)

    print(
        f'Produto "{item["nome"]}" adicionado '
        f'com quantidade {quantity} e preço unitário '
        f'R$ {price:.2f}.'
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



def edit_price(items):
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

        price_input = input('Digite o novo preço unitário (R$): ')
        price_input = price_input.strip().replace(',', '.')

        try:
            price = Decimal(price_input)

            if not price.is_finite() or price < 0:
                print('O preço deve ser válido e não negativo.')
                return False

            if price.as_tuple().exponent < -2:
                print('O preço deve ter no máximo duas casas decimais.')
                return False

        except InvalidOperation:
            print('Digite um preço válido.')
            return False

        old_price = Decimal(item.get('preco', '0.00'))
        item['preco'] = str(price)

        print(
            f'Preço de "{item["nome"]}" atualizado '
            f'de R$ {old_price:.2f} para R$ {price:.2f}.'
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

        price = Decimal(item.get('preco', '0.00'))
        subtotal = price * item['quantidade']

        print(
            f'{index}. {item["nome"]} '
            f'- Quantidade: {item["quantidade"]} '
            f'- Preço unitário: R$ {price:.2f} '
            f'- Subtotal: R$ {subtotal:.2f} '
            f'- {status}'
        )

    print('-' * 30)
    print(f'TOTAL GERAL: R$ {calculate_total(items):.2f}')
    print(f'TOTAL PENDENTE: R$ {calculate_pending_total(items):.2f}')
    print('-' * 30)


def filter_items(items):
    if not items:
        print('Sua lista está vazia.')
        return

    print('\n--- FILTRAR PRODUTOS ---')
    print('[T] Todos os produtos')
    print('[P] Produtos pendentes')
    print('[C] Produtos comprados')

    option = input('Escolha uma opção: ').strip().upper()

    if option == 'T':
        filtered_items = items

    elif option == 'P':
        filtered_items = [
            item for item in items
            if not item['comprado']
        ]

    elif option == 'C':
        filtered_items = [
            item for item in items
            if item['comprado']
        ]

    else:
        print('Opção inválida.')
        return

    if not filtered_items:
        print('Nenhum produto encontrado para esse filtro.')
        return

    list_items(filtered_items)


def command_terminal(option, items):
    if option == 'I':
        return add_item(items)

    elif option == 'A':
        return remove_item(items)

    elif option == 'Q':
        return edit_quantity(items)

    elif option == 'P':
        return edit_price(items)

    elif option == 'M':
        return toggle_purchased(items)

    elif option == 'L':
        list_items(items)

    elif option == 'F':
        filter_items(items)

    return False


def calculate_total(items):
    total = Decimal('0.00')

    for item in items:
        price = Decimal(item.get('preco', '0.00'))
        subtotal = price * item['quantidade']
        total += subtotal

    return total


def calculate_pending_total(items):
    total = Decimal('0.00')

    for item in items:
        if not item['comprado']:
            price = Decimal(item.get('preco', '0.00'))
            subtotal = price * item['quantidade']
            total += subtotal

    return total