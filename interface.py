import customtkinter as ctk
from decimal import Decimal
from features import create_item
from package_data.data_features import load_data, save_data


class ShoppingListApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Lista de Compras")
        self.geometry("1000x650")
        self.minsize(800, 550)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.items = load_data()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Menu lateral
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="SHOPPING LIST",
            font=("Arial", 20, "bold")
        )
        self.logo.pack(pady=30)

        self.btn_lista = ctk.CTkButton(
            self.sidebar, text="Lista de Compras"
        )
        self.btn_lista.pack(fill="x", padx=15, pady=10)

        self.btn_relatorios = ctk.CTkButton(
            self.sidebar, text="Relatórios"
        )
        self.btn_relatorios.pack(fill="x", padx=15, pady=10)

        self.btn_config = ctk.CTkButton(
            self.sidebar, text="Configurações"
        )
        self.btn_config.pack(fill="x", padx=15, pady=10)

        # Área principal
        self.main_area = ctk.CTkFrame(self, corner_radius=0)
        self.main_area.grid(row=0, column=1, sticky="nsew")

        self.main_area.grid_columnconfigure(0, weight=1)

        # Cabeçalho
        self.title_label = ctk.CTkLabel(
            self.main_area,
            text="Minha Lista de Compras",
            font=("Arial", 28, "bold")
        )
        self.title_label.pack(anchor="w", padx=30, pady=(30, 5))

        self.description = ctk.CTkLabel(
            self.main_area,
            text="Gerencie seus produtos e acompanhe suas compras.",
            font=("Arial", 14)
        )
        self.description.pack(anchor="w", padx=30, pady=(0, 20))

        # Cabeçalho da tabela
        self.table_header = ctk.CTkFrame(self.main_area)
        self.table_header.pack(fill="x", padx=30, pady=10)

        columns = ["Produto", "Quantidade", "Preço", "Status"]

        for index, column in enumerate(columns):
            self.table_header.grid_columnconfigure(
                index,
                weight=1,
                uniform="colunas"
            )
            label = ctk.CTkLabel(
                self.table_header,
                text=column,
                font=("Arial", 14, "bold")
            )
            label.grid(row=0, column=index, sticky="ew", padx=10, pady=12)

        # Área onde os produtos serão exibidos
        self.products_frame = ctk.CTkScrollableFrame(
            self.main_area,
            label_text="Produtos cadastrados"
        )
        self.products_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        self.refresh_products()

        # Botão adicionar
        self.add_button = ctk.CTkButton(
            self.main_area,
            text="+ Adicionar produto",
            height=40,
            command=self.open_add_product
        )
        self.add_button.pack(
            anchor="e",
            padx=30,
            pady=20
        )


    def open_add_product(self):
        # Verificar se a janela já está aberta
        if hasattr(self, "add_window") and self.add_window.winfo_exists():
            self.add_window.lift()
            self.add_window.focus_force()
            return


        # Criar uma nova janela
        self.add_window = ctk.CTkToplevel(self)
        self.add_window.title("Adicionar produto")
        self.add_window.geometry("400x350")
        self.add_window.resizable(False, False)
        self.add_window.transient(self)
        self.add_window.grab_set()
        self.add_window.lift()

        # Título
        title = ctk.CTkLabel(
            self.add_window,
            text="Cadastrar produto",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=20)

        # Campo nome
        self.name_entry = ctk.CTkEntry(
            self.add_window,
            placeholder_text="Nome do produto",
            width=300
        )
        self.name_entry.pack(pady=10)

        # Campo quantidade
        self.quantity_entry = ctk.CTkEntry(
            self.add_window,
            placeholder_text="Quantidade",
            width=300
        )
        self.quantity_entry.pack(pady=10)

        # Campo preço
        self.price_entry = ctk.CTkEntry(
            self.add_window,
            placeholder_text="Preço unitário",
            width=300
        )
        self.price_entry.pack(pady=10)

        self.form_feedback = ctk.CTkLabel(
            self.add_window,
            text="",
            text_color="red"
        )
        self.form_feedback.pack(pady=5)

        # Botão salvar
        save_button = ctk.CTkButton(
            self.add_window,
            text="Salvar produto",
            command=self.save_product
        )
        save_button.pack(pady=10)


    def save_product(self):
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        success, message = create_item(
            self.items,
            name,
            quantity,
            price
        )

        if not success:
            self.form_feedback.configure(
                text=message,
                text_color="red"
            )
            return

        # Salvar os produtos no arquivo JSON
        if not save_data(self.items):
            self.items.pop()

            self.form_feedback.configure(
                text="Erro ao salvar o produto.",
                text_color="red"
            )
            return

        self.refresh_products()
        self.add_window.destroy()


    def refresh_products(self):
        # Limpar os produtos exibidos anteriormente
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        # Exibir os produtos cadastrados
        for item in self.items:
            row = ctk.CTkFrame(self.products_frame)
            row.pack(fill="x", padx=5, pady=5)

            # Configurar as quatro colunas
            for column in range(4):
                row.grid_columnconfigure(
                    column,
                    weight=1,
                    uniform="colunas"
                )

            price = Decimal(item["preco"])
            status = "Comprado" if item["comprado"] else "Pendente"

            values = [
                item["nome"],
                str(item["quantidade"]),
                f"R$ {price:.2f}",
                status
            ]

            for index, value in enumerate(values):
                label = ctk.CTkLabel(
                    row,
                    text=value
                )
                label.grid(
                    row=0,
                    column=index,
                    sticky="ew",
                    padx=10,
                    pady=12
                )

if __name__ == "__main__":
    app = ShoppingListApp()
    app.mainloop()
