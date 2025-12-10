from typing import Optional

class TransactionNode:
    """
    Node buat Doubly Linked List
    Setiap node merepresentasikan satu transaksi dengan pointer ke node prev/next
    
    Attributes:
        date (str): Transaction date in YYYY-MM-DD format
        title (str): Transaction description
        amount (float): Transaction amount
        trans_type (str): Either "Income" or "Expense"
        category (str): Transaction category
        trans_id (int): Unique identifier
        is_recurring (bool): Whether this is a recurring transaction
        recurrence_type (str): "monthly", "weekly", or None if not recurring
        next: Pointer to next node in DLL
        prev: Pointer to previous node in DLL
    """
    
    def __init__(self, date: str, title: str, amount: float, 
                 trans_type: str, category: str, trans_id: int,
                 is_recurring: bool = False, recurrence_type: Optional[str] = None):
        self.date = date
        self.title = title
        self.amount = amount
        self.trans_type = trans_type
        self.category = category
        self.trans_id = trans_id
        self.is_recurring = is_recurring
        self.recurrence_type = recurrence_type  # "monthly" or "weekly"
        
        # Doubly Linked List Pointers
        self.next: Optional[TransactionNode] = None
        self.prev: Optional[TransactionNode] = None
    
    def to_dict(self) -> dict:
        """
        Konversi node ke dictionary untuk serialisasi JSON
        Returns:
            Dictionary representation of the transaction
        """
        return {
            "id": self.trans_id,
            "date": self.date,
            "title": self.title,
            "amount": self.amount,
            "type": self.trans_type,
            "category": self.category,
            "is_recurring": self.is_recurring,
            "recurrence_type": self.recurrence_type
        }
    
    def __str__(self) -> str:
        """Representation string buat debugging"""
        return f"{self.trans_type}: {self.title} - Rp {self.amount:,.0f}"