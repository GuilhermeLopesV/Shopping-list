# 🛒 Shopping List Manager

A shopping list manager developed in **Python** that runs in the terminal. The project allows users to organize their shopping lists, manage product quantities and prices, track purchased items, and calculate shopping costs.

This project was developed to practice Python programming, modular code organization, data persistence, input validation, and automated testing.

## ✨ Features

- **Add Items:** Add products with names, quantities, and unit prices.
- **Delete Items:** Remove products from the shopping list.
- **List Items:** Display all products, including their quantities, prices, and purchase status.
- **Filter Items:** Filter products based on their purchase status.
- **Edit Quantities:** Update the quantity of existing products.
- **Edit Prices:** Change product prices whenever necessary.
- **Mark as Purchased:** Toggle the purchase status of individual items.
- **Cost Calculation:** Calculate the total shopping cost and the amount corresponding to pending items.
- **Data Persistence:** Automatically save and load shopping list data using JSON.
- **Input Validation:** Validate product names, quantities, prices, and menu options.
- **Error Handling:** Handle invalid input, missing files, and JSON-related errors.
- **Automated Tests:** Verify application functionality using Python's `unittest` framework.

## 🛠️ Technologies

- **Python 3** — Application logic and functionality.
- **JSON** — Local data storage and persistence.
- **unittest** — Automated testing.
- **Git & GitHub** — Version control and project management.

## 📁 Project Structure

```text
Shopping-list/
│
├── main.py
├── features.py
│
├── package_data/
│   └── data_features.py
│
├── tests/
│   └── ...
│
├── history.json
└── README.md
```

- `main.py`: Application entry point and terminal menu.
- `features.py`: Shopping list operations and business logic.
- `package_data/`: Data loading, saving, and persistence functionality.
- `tests/`: Automated tests.
- `history.json`: Local storage for shopping list data.

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or later recommended.
- Git (optional, for cloning the repository).

### Installation

1. Clone the repository:

```bash
git clone https://github.com/GuilhermeLopesV/Shopping-list.git
```

2. Navigate to the project directory:

```bash
cd Shopping-list
```

3. Run the application:

```bash
python main.py
```

## 💻 How to Use

After starting the application, choose an option from the terminal menu:

| Option | Action |
|:---:|---|
| `I` | Insert a new item |
| `A` | Delete an item |
| `L` | List all items |
| `F` | Filter items |
| `Q` | Edit item quantity |
| `P` | Edit item price |
| `M` | Mark or unmark an item as purchased |
| `E` | Exit the program |

Your shopping list is stored locally in a JSON file, allowing your data to remain available between executions.

## 🧪 Running Tests

The project uses Python's built-in `unittest` framework.

To execute the automated tests, run:

```bash
python -m unittest discover -s tests -v
```

## 📚 Learning Goals

This project provides practical experience with:

- Python functions and modular programming.
- Data structures such as lists and dictionaries.
- Conditional statements, loops, and user input.
- Input validation and exception handling.
- Reading and writing JSON files.
- Data persistence and file management.
- Automated testing with `unittest`.
- Code organization and maintainability.

## 🔮 Future Improvements

- Develop a graphical user interface (GUI).
- Implement product search and sorting.
- Add reports and shopping history.
- Improve the user experience and interface.

## 👨‍💻 Author

**Guilherme Lopes V.**

[GitHub Profile](https://github.com/GuilhermeLopesV)

---

*This project is part of my journey in software development and continuous learning with Python.*