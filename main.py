import os
import sys
from models import Transaction
from data_manager import DataManager
from summary_manager import SummaryManager
summary_manager = SummaryManager()
from settings_manager import SettingsManager
settings_manager = SettingsManager()

class PersonalFinanceApp:
    """
    Main class for personal finance application
    """
    
    def __init__(self):
        self.data_manager = DataManager()
        self.running = True
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("           PERSONAL FINANCE APPLICATION")
        print("="*50)
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Transactions")
        print("4. Balance Status")
        print("5. Monthly Summary(current month)")
        print("6. Set Monthly Limit")
        print("7. Exit")
        print("="*50)
    
    def get_transaction_input(self, transaction_type: str) -> Transaction:
        """Get transaction information from user"""
        print(f"\n{transaction_type.upper()} INFORMATION")
        print("-" * 30)
        
        while True:
            try:
                amount = float(input("Amount (TL): "))
                if amount <= 0:
                    print("Amount must be greater than zero!")
                    continue
                break
            except ValueError:
                print("Please enter a valid number!")
        
        category = input("Category: ").strip()
        while not category:
            print("Category cannot be empty!")
            category = input("Category: ").strip()
        
        description = input("Description: ").strip()
        while not description:
            print("Description cannot be empty!")
            description = input("Description: ").strip()
        
        return Transaction(amount, category, description, transaction_type)
    
    def add_income(self):
        """Add income process"""
        try:
            transaction = self.get_transaction_input("income")
            if self.data_manager.add_transaction(transaction):
                print(f"\n✅ Income successfully added: {transaction.amount} TL")
                summary_manager.update_summary(transaction)
            else:
                print("\n❌ An error occurred while adding income!")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def add_expense(self):
        """Add expense process"""
        try:
            transaction = self.get_transaction_input("expense")
            if self.data_manager.add_transaction(transaction):
                print(f"\n✅ Expense successfully added: {transaction.amount} TL")
                summary_manager.update_summary(transaction)
            else:
                print("\n❌ An error occurred while adding expense!")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        # Limit control
        from datetime import datetime
        current_month = datetime.now().strftime("%Y-%m")
        monthly_summary = summary_manager.get_summary(current_month)
        limit = settings_manager.get_monthly_limit()

        if limit > 0 and monthly_summary["expense"] > limit:
            print(f"\n⚠️ Warning: You have exceeded your monthly limit of {limit:,.2f} TL!")
        
        input("\nPress Enter to continue...")
    
    def display_transactions(self):
        """Display all transactions"""
        transactions = self.data_manager.get_all_transactions()
        
        if not transactions:
            print("\n📋 No transactions recorded yet.")
        else:
            print(f"\n📋 TOTAL {len(transactions)} TRANSACTIONS")
            print("-" * 70)
            
            # Incomes
            incomes = self.data_manager.get_transactions_by_type("income")
            if incomes:
                print("\n💰 INCOMES:")
                for income in incomes[-10:]:  # Last 10 incomes
                    print(f"   {income}")
            
            # Expenses
            expenses = self.data_manager.get_transactions_by_type("expense")
            if expenses:
                print("\n💸 EXPENSES:")
                for expense in expenses[-10:]:  # Last 10 expenses
                    print(f"   {expense}")
            
            if len(transactions) > 20:
                print(f"\n... (Showing last 20 transactions, total: {len(transactions)})")
        
        input("\nPress Enter to continue...")
    
    def display_balance(self):
        """Display balance status"""
        balance_info = self.data_manager.get_balance()
        
        print("\n💼 BALANCE STATUS")
        print("=" * 40)
        print(f"💰 Total Income : {balance_info['total_income']:,.2f} TL")
        print(f"💸 Total Expense: {balance_info['total_expense']:,.2f} TL")
        print("-" * 40)
        
        balance = balance_info['balance']
        if balance >= 0:
            print(f"✅ Net Balance  : +{balance:,.2f} TL")
        else:
            print(f"❌ Net Balance  : {balance:,.2f} TL")
        
        print("=" * 40)
        
        # Category summary
        categories = self.data_manager.get_categories()
        if categories['income_categories']:
            print(f"\n📊 Income Categories: {', '.join(categories['income_categories'])}")
        if categories['expense_categories']:
            print(f"📊 Expense Categories: {', '.join(categories['expense_categories'])}")
        
        input("\nPress Enter to continue...")
    
    def display_monthly_summary(self):
        """Display income, expense and net total for current month"""
        from datetime import datetime
        current_month = datetime.now().strftime("%Y-%m")
        summary = summary_manager.get_summary(current_month)

        print(f"\n📆 Monthly Summary - {current_month}")
        print("=" * 40)
        print(f"💰 Income : {summary['income']:,.2f} TL")
        print(f"💸 Expense: {summary['expense']:,.2f} TL")
    
        net = summary["net"]
        if net >= 0:
            print(f"📊 Net     : +{net:,.2f} TL ✅")
        else:
            print(f"📊 Net     : {net:,.2f} TL ❌")
        print("=" * 40)

        input("\nPress Enter to continue...")    

    def set_monthly_limit(self):
        """Set or update the monthly spending limit"""
        print("\n⚙️  Set Monthly Spending Limit")
        print("-" * 40)
        try:
            limit = float(input("Enter new monthly limit (TL): "))
            if settings_manager.set_monthly_limit(limit):
                print(f"\n✅ Monthly limit set to {limit:,.2f} TL")
            else:
                print("\n❌ Failed to update monthly limit.")
        except ValueError:
            print("\n❌ Invalid input. Please enter a number.")
        input("\nPress Enter to continue...")

    def run(self):
        """Run the application"""
        print("Starting Personal Finance Application...")
        
        while self.running:
            self.clear_screen()
            self.display_menu()
            
            try:
                choice = input("\nMake your choice (1-7): ").strip()
                
                if choice == "1":
                    self.add_income()
                elif choice == "2":
                    self.add_expense()
                elif choice == "3":
                    self.display_transactions()
                elif choice == "4":
                    self.display_balance()
                elif choice == "5":
                    self.display_monthly_summary()
                elif choice == "6":
                    self.set_monthly_limit()
                elif choice == "7":
                    print("\n👋 Exiting application. Have a good day!")
                    self.running = False
                else:
                    print("\n❌ Invalid choice! Please enter a number between 1-7.")
                    input("Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Terminating application...")
                self.running = False
            except Exception as e:
                print(f"\n❌ An unexpected error occurred: {e}")
                input("Press Enter to continue...")

def main():
    """Main function"""
    app = PersonalFinanceApp()
    app.run()

if __name__ == "__main__":
    main()