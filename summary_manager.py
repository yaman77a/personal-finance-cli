import json
import os
from datetime import datetime
from typing import Dict, Optional
from models import Transaction

class SummaryManager:
    """
    Class for managing monthly summaries of all transactions
    """
    
    def __init__(self, filename: str = "monthly_summary.json"):
        self.filename = filename
        self.summary_data = {}
        self._ensure_file_exists()
        self.load_summary()
    
    def _ensure_file_exists(self):
        """Ensure JSON file exists, create if it doesn't"""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
    
    def _extract_month_from_date(self, date_string: str) -> str:
        """
        Extract month in YYYY-MM format from date string
        Expected format: "YYYY-MM-DD HH:MM:SS"
        """
        try:
            # Parse the date and extract year-month
            date_obj = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
            return date_obj.strftime("%Y-%m")
        except ValueError:
            # Fallback: try to extract manually if format is different
            return date_string[:7]  # Assumes YYYY-MM-DD format at minimum
    
    def load_summary(self) -> Dict:
        """
        Read the summary JSON file and load it as a dictionary
        Returns the loaded summary data
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.summary_data = json.load(f)
                return self.summary_data
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Summary loading error: {e}")
            self.summary_data = {}
            return {}
    
    def save_summary(self, summary_data: Dict) -> bool:
        """
        Save the dictionary to monthly_summary.json
        """
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(summary_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Summary saving error: {e}")
            return False
    
    def update_summary(self, transaction: Transaction) -> bool:
        """
        Takes a Transaction object, extracts the month from the transaction's date,
        updates the monthly income or expense accordingly, and saves to JSON file
        """
        try:
            # Extract month from transaction date
            month = self._extract_month_from_date(transaction.date)
            
            # Initialize month data if it doesn't exist
            if month not in self.summary_data:
                self.summary_data[month] = {
                    "income": 0.0,
                    "expense": 0.0,
                    "net": 0.0
                }
            
            # Update the appropriate field based on transaction type
            if transaction.transaction_type == "income":
                self.summary_data[month]["income"] += transaction.amount
            elif transaction.transaction_type == "expense":
                self.summary_data[month]["expense"] += transaction.amount
            
            # Recalculate net balance for the month
            self.summary_data[month]["net"] = (
                self.summary_data[month]["income"] - 
                self.summary_data[month]["expense"]
            )
            
            # Save updated data
            return self.save_summary(self.summary_data)
            
        except Exception as e:
            print(f"Error updating summary: {e}")
            return False
    
    def get_summary(self, month: str) -> Dict[str, float]:
        """
        Returns the summary of a given month in the form:
        {"income": float, "expense": float, "net": float}
        If month doesn't exist, returns zeros
        """
        if month in self.summary_data:
            return self.summary_data[month].copy()
        else:
            # Return default values if month doesn't exist
            return {
                "income": 0.0,
                "expense": 0.0,
                "net": 0.0
            }
    
    def get_all_months(self) -> list:
        """
        Return a list of all months that have summary data
        """
        return sorted(self.summary_data.keys())
    
    def get_yearly_summary(self, year: str) -> Dict[str, float]:
        """
        Calculate yearly totals for a given year
        """
        yearly_income = 0.0
        yearly_expense = 0.0
        
        for month, data in self.summary_data.items():
            if month.startswith(year):
                yearly_income += data["income"]
                yearly_expense += data["expense"]
        
        return {
            "income": yearly_income,
            "expense": yearly_expense,
            "net": yearly_income - yearly_expense
        }
    
    def delete_month_summary(self, month: str) -> bool:
        """
        Delete summary data for a specific month
        """
        try:
            if month in self.summary_data:
                del self.summary_data[month]
                return self.save_summary(self.summary_data)
            return True  # Month doesn't exist, consider it successful
        except Exception as e:
            print(f"Error deleting month summary: {e}")
            return False
    
    def rebuild_summary_from_transactions(self, transactions: list) -> bool:
        """
        Rebuild the entire summary from a list of Transaction objects
        Useful for data consistency checks or migrations
        """
        try:
            # Reset summary data
            self.summary_data = {}
            
            # Process each transaction
            for transaction in transactions:
                month = self._extract_month_from_date(transaction.date)
                
                # Initialize month if it doesn't exist
                if month not in self.summary_data:
                    self.summary_data[month] = {
                        "income": 0.0,
                        "expense": 0.0,
                        "net": 0.0
                    }
                
                # Add transaction amount to appropriate category
                if transaction.transaction_type == "income":
                    self.summary_data[month]["income"] += transaction.amount
                elif transaction.transaction_type == "expense":
                    self.summary_data[month]["expense"] += transaction.amount
                
                # Recalculate net
                self.summary_data[month]["net"] = (
                    self.summary_data[month]["income"] - 
                    self.summary_data[month]["expense"]
                )
            
            # Save the rebuilt data
            return self.save_summary(self.summary_data)
            
        except Exception as e:
            print(f"Error rebuilding summary: {e}")
            return False