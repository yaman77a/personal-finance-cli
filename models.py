from datetime import datetime
from typing import Literal

class Transaction:
    """
    Class representing income and expense transactions
    """
    
    def __init__(self, amount: float, category: str, description: str, 
                 transaction_type: Literal["income", "expense"]):
        self.id = self._generate_id()
        self.amount = amount
        self.category = category
        self.description = description
        self.transaction_type = transaction_type
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _generate_id(self) -> str:
        """Generate unique ID"""
        return datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    def to_dict(self) -> dict:
        """Convert Transaction object to dictionary"""
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "transaction_type": self.transaction_type,
            "date": self.date
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create Transaction object from dictionary"""
        transaction = cls(
            amount=data["amount"],
            category=data["category"],
            description=data["description"],
            transaction_type=data["transaction_type"]
        )
        transaction.id = data["id"]
        transaction.date = data["date"]
        return transaction
    
    def __str__(self) -> str:
        """Return string representation of Transaction object"""
        return (f"{self.transaction_type.upper()}: {self.amount} TL - "
                f"{self.category} - {self.description} ({self.date})")