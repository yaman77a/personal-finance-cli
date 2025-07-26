# Personal Finance CLI App

A simple terminal-based personal finance tracker.
You can add income and expenses, view your balance, and list transactions with descriptions.

---

## Features

- [x] Add income and expenses with descriptions
- [x] View all transactions with descriptions
- [x] See current balance
- [] Monthly/Yearly balance (coming soon)
- [] Expense category statistics (planned)
- [] Visulation with matplotlib (planned)
- [] Regular monthly expenses and incomes (planned)
- [] Warning when approaching the limit (planned)
- [] Expense Analyzer with AI support (planned)
- [] Currency Converter (planned)
- [] GUI version (planned)

---

## Project Info

- Written in **Python 3**
- Data is saved locally in 'transaction.json'
- Terminal inerface only (CLI) for now
- Organized into 3 modules:
    - 'main.py' -> user interaction 
    - 'models.py' -> transaction class
    - 'data_manager.py' -> JSON file handling (read/write)

---

## Notes

- I initially brainstormed the idea with **ChatGPT**, and used **Claude** to generate the first version of the code.I then custimozed some minor things myself.
- This is part of my personal learning journey as a CS student interested in Python, finance, and software design.


---

## Planned Next Steps

- Add the features listed above (limits, stats, AI, etc.)
- Build a GUI version (Tkinter / PyQt)
- Possibly move from JSON to SQLite in the future

---

## How to Run

```bash
git clone https://github.com/yaman77a/personal-finance-cli.git
cd personal-finance-cli
python3 main.py