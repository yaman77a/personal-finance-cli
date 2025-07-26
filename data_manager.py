import json
import os
from typing import List, Dict, Any
from models import Transaction

class DataManager:
    """
    Class managing data read/write operations with JSON file
    """
    
    def __init__(self, filename: str = "transactions.json"):
        self.filename = filename
        self.transactions = []
        self._ensure_file_exists()
        self.load_transactions()
    
    def _ensure_file_exists(self):
        """Ensure JSON file exists, create if it doesn't"""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def load_transactions(self) -> List[Transaction]:
        """Load transactions from JSON file"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.transactions = [Transaction.from_dict(item) for item in data]
                return self.transactions
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Data loading error: {e}")
            self.transactions = []
            return []
    
    def save_transactions(self) -> bool:
        """Save transactions to JSON file"""
        try:
            data = [transaction.to_dict() for transaction in self.transactions]
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Data saving error: {e}")
            return False
    
    def add_transaction(self, transaction: Transaction) -> bool:
        """Add a new transaction"""
        try:
            self.transactions.append(transaction)
            return self.save_transactions()
        except Exception as e:
            print(f"Transaction adding error: {e}")
            return False
    
    def get_all_transactions(self) -> List[Transaction]:
        """Return all transactions"""
        return self.transactions
    
    def get_transactions_by_type(self, transaction_type: str) -> List[Transaction]:
        """Return transactions of specific type"""
        return [t for t in self.transactions if t.transaction_type == transaction_type]
    
    def get_balance(self) -> Dict[str, float]:
        """Calculate total income, expense and balance"""
        total_income = sum(t.amount for t in self.transactions if t.transaction_type == "income")
        total_expense = sum(t.amount for t in self.transactions if t.transaction_type == "expense")
        balance = total_income - total_expense
        
        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance
        }
    
    def get_categories(self) -> Dict[str, List[str]]:
        """Return income and expense categories"""
        income_categories = list(set(t.category for t in self.transactions 
                                   if t.transaction_type == "income"))
        expense_categories = list(set(t.category for t in self.transactions 
                                    if t.transaction_type == "expense"))
        
        return {
            "income_categories": income_categories,
            "expense_categories": expense_categories
        }