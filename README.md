# Personal Finance CLI App

A simple terminal-based personal finance tracker.
You can add income and expenses, view your balance, and list transactions with descriptions.

---

## Features

- [x] Add income and expenses with descriptions
- [x] View all transactions with descriptions
- [x] See current balance
- [x] Monthly balance
- [x] Set a monthly expense limit and get warnings when exceeded
- [] Expense category statistics (planned)
- [] Visulation with matplotlib (planned)
- [] Regular monthly expenses and incomes (planned)
- [] Expense Analyzer with AI support (planned)
- [] Currency Converter (planned)
- [] GUI version (planned)

---

## Project Info

- Written in **Python 3**
- Data is saved locally in 
    - 'transaction.json'
    - 'monthly_summary.json'
    - 'settings.json'
- Terminal inerface only (CLI) for now
- Organized into 5 modules:
    - 'main.py' -> user interaction 
    - 'models.py' -> transaction class
    - 'data_manager.py' -> JSON file handling (read/write)
    - 'summary_manager.py' -> handle monthly summaries
    - 'settings_manager.py' -> manage monthly limit

---

## Notes

- I initially brainstormed the idea with **ChatGPT**, and used **Claude** to generate the first version of the code. I then custimozed some minor things myself.


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
