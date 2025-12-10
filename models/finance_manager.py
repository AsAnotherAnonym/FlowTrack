import json
import os
import csv
from models.max_heap import MaxHeap
from models.transaction_node import TransactionNode
from models.recurring_queue import RecurringTransactionQueue
from models.budget_bst import BudgetBST
from typing import Optional, Dict, List
from datetime import datetime

class FinanceManager:
    """
    Backend Manager Class - Core Business Logic
    
    Struktur data yang digunakan:
    1. Doubly Linked List - Menyimpan transaksi sesuai urutan insertion
    2. Max-Heap - Melacak pengeluaran tertinggi
    3. Hash Map - Mengelompokkan transaksi berdasarkan tanggal
    
    Responsibilities:
        - Operasi CRUD pada transaksi
        - Manajemen Strukdata
        - Penyimpanan file (JSON)
        - Perhitungan statistik
    """
    
    def __init__(self, data_file: str = "data.json"):
        """
        Inisialisasi Finance Manager
        
        Args:
            data_file: Path to JSON file for data persistence
        """
        self.data_file = data_file
        
        # DOUBLY LINKED LIST
        self.head: Optional[TransactionNode] = None
        self.tail: Optional[TransactionNode] = None
        self.transaction_count = 0
        
        # MAX-HEAP
        self.expense_heap = MaxHeap()
        
        # RECURRING TRANSACTIONS QUEUE
        self.recurring_queue = RecurringTransactionQueue()
        
        # BUDGET BST
        self.budget_bst = BudgetBST()
        
        # Statistics
        self.total_income = 0.0
        self.total_expense = 0.0
        
        # Load existing data
        self.load_from_file()
    
    # ==================== DLL OPERATIONS ====================
    
    def insert_at_head(self, date: str, title: str, amount: float, 
                       trans_type: str, category: str, 
                       is_recurring: bool = False, 
                       recurrence_type: Optional[str] = None) -> TransactionNode:
        """
        Memasukkan transaksi baru di awal Doubly Linked List (DLL)
        Sehingga memastikan transaksi terbaru muncul di urutan pertama.
        
        Time Complexity: O(1) + O(1) if recurring transaction
        
        Args:
            date: Transaction date (YYYY-MM-DD)
            title: Transaction description
            amount: Transaction amount
            trans_type: "Income" or "Expense"
            category: Transaction category
            is_recurring: Whether this is a recurring transaction
            recurrence_type: "monthly" or "weekly" if is_recurring=True
        
        Returns:
            The newly created TransactionNode
        """
        self.transaction_count += 1
        new_node = TransactionNode(date, title, amount, trans_type, 
                                   category, self.transaction_count,
                                   is_recurring, recurrence_type)
        
        if not self.head:  # Empty list
            self.head = self.tail = new_node
        else:
            # Insert at head
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        
        # Update statistics
        if trans_type == "Income":
            self.total_income += amount
        else:
            self.total_expense += amount
            # INSERT INTO MAX-HEAP
            self.expense_heap.insert(amount, new_node)
        
        # Schedule recurring transaction if applicable
        if is_recurring and recurrence_type:
            self.recurring_queue.schedule_recurring_transaction(new_node, date)
        
        return new_node
    
    def delete_node(self, node: TransactionNode) -> bool:
        """
        Menghaous node dari Doubly Linked List (DLL)
        
        Time Complexity: O(1) for deletion + O(n) for heap rebuild if expense
        
        Args:
            node: The node to delete
        
        Returns:
            True if deletion was successful
        """
        if not node:
            return False
        
        # Update statistics
        if node.trans_type == "Income":
            self.total_income -= node.amount
        else:
            self.total_expense -= node.amount
        
        # Handle DLL pointers
        if node.prev:
            node.prev.next = node.next
        else:  # node is head
            self.head = node.next
        
        if node.next:
            node.next.prev = node.prev
        else:  # node is tail
            self.tail = node.prev
        
        # Rebuild heap if expense was deleted
        if node.trans_type == "Expense":
            self.expense_heap.rebuild_from_dll(self.head)
        
        return True
    
    def update_node(self, node: TransactionNode, date: str = None, 
                   title: str = None, amount: float = None, 
                   trans_type: str = None, category: str = None) -> bool:
        """
        Update node di DLL tanpa delete-insert (in-place update)
        Cocok untuk demo: menunjukkan operasi update pada DLL
        
        Time Complexity: O(1) + O(n) if expense amount changed (heap rebuild)
        
        Args:
            node: The node to update
            date: New date (optional)
            title: New title (optional)
            amount: New amount (optional)
            trans_type: New transaction type (optional)
            category: New category (optional)
        
        Returns:
            True if update was successful
        """
        if not node:
            return False
        
        old_amount = node.amount
        old_type = node.trans_type
        
        # Update fields (hanya yang disediakan)
        if date is not None:
            node.date = date
        if title is not None:
            node.title = title
        if category is not None:
            node.category = category
        if trans_type is not None:
            node.trans_type = trans_type
        
        # Handle amount change (update statistics)
        if amount is not None and amount != old_amount:
            # Adjust old statistics
            if old_type == "Income":
                self.total_income -= old_amount
            else:
                self.total_expense -= old_amount
            
            # Add new statistics
            if trans_type == "Income" or (trans_type is None and old_type == "Income"):
                self.total_income += amount
            else:
                self.total_expense += amount
            
            # Update amount
            node.amount = amount
            
            # Rebuild heap if expense amount changed
            if (old_type == "Expense" or 
                (trans_type == "Expense" and trans_type is not None)):
                self.expense_heap.rebuild_from_dll(self.head)
        
        return True
    
    def export_to_csv(self, filename: str = "transactions_export.csv") -> bool:
        """
        Export semua transaksi ke file CSV dengan traversal DLL
        Good for demo: menunjukkan traversal DLL ke professor
        
        Time Complexity: O(n) dimana n adalah jumlah transaksi
        
        Args:
            filename: Output CSV filename
        
        Returns:
            True if export was successful
        """
        try:
            current = self.head
            transactions = []
            
            # Traverse DLL dan collect data
            while current:
                transactions.append({
                    'ID': current.trans_id,
                    'Date': current.date,
                    'Title': current.title,
                    'Amount': current.amount,
                    'Type': current.trans_type,
                    'Category': current.category,
                    'Recurring': 'Yes' if current.is_recurring else 'No',
                    'Recurrence Type': current.recurrence_type or '-'
                })
                current = current.next
            
            # Reverse to maintain chronological order
            transactions.reverse()
            
            # Write to CSV
            if transactions:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=[
                        'ID', 'Date', 'Title', 'Amount', 'Type', 'Category', 
                        'Recurring', 'Recurrence Type'
                    ])
                    writer.writeheader()
                    writer.writerows(transactions)
                
                return True
            else:
                # Create empty CSV if no transactions
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=[
                        'ID', 'Date', 'Title', 'Amount', 'Type', 'Category', 
                        'Recurring', 'Recurrence Type'
                    ])
                    writer.writeheader()
                
                return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
    
    def find_node_by_id(self, trans_id: int) -> Optional[TransactionNode]:
        """
        Menelusuri DLL untuk menemukan node berdasarkan ID
        
        Time Complexity: O(n)
        
        Args:
            trans_id: Transaction ID to find
        
        Returns:
            TransactionNode if found, None otherwise
        """
        current = self.head
        while current:
            if current.trans_id == trans_id:
                return current
            current = current.next
        return None
    
    def get_all_transactions(self) -> List[TransactionNode]:
        """
        Mendapatkan semua transaksi sebagai daftar (menelusuri DLL)
        
        Time Complexity: O(n)
        
        Returns:
            List of all TransactionNodes
        """
        transactions = []
        current = self.head
        while current:
            transactions.append(current)
            current = current.next
        return transactions
    
    # ==================== HASH MAP ====================
    
    def group_by_date(self) -> Dict[str, List[TransactionNode]]:
        """
        Mengelompokkan transaksi berdasarkan tanggal menggunakan Hash Map (Dictionary)
        
        Menunjukkan struktur data Hash Map di mana:
        - Key: Date string (contoh, "2024-12-05")
        - Value: List of TransactionNode objects for that date
        
        Time Complexity: O(n) dimana n adalah jumlah total transaksi
        Space Complexity: O(n)
        
        Returns:
            Dictionary mapping dates to lists of transactions
        """
        date_map: Dict[str, List[TransactionNode]] = {}
        
        # Menelusuri DLLnya
        current = self.head
        while current:
            date_key = current.date
            
            # Hash Map operation: check if key exists
            if date_key not in date_map:
                date_map[date_key] = []
            
            # Hash Map operation: append to value list
            date_map[date_key].append(current)
            current = current.next
        
        return date_map
    
    # ==================== HEAP ====================
    
    def get_highest_expense(self) -> Optional[TransactionNode]:
        """
        Mendapatkan highest expense dari Max-Heap
        
        Time Complexity: O(1)
        
        Returns:
            TransactionNode with highest expense, or None if no expenses
        """
        return self.expense_heap.get_max()
    
    # ==================== STATISTIK ====================
    
    def get_balance(self) -> float:
        """
        Menghitung balance (Income - Expense)
        
        Returns:
            Current balance
        """
        return self.total_income - self.total_expense
    
    def get_stats(self) -> Dict[str, float]:
        """
        Get semua statistik keuangan
        
        Returns:
            Dictionary with balance, income, expense, and highest_expense
        """
        highest = self.get_highest_expense()
        return {
            "balance": self.get_balance(),
            "total_income": self.total_income,
            "total_expense": self.total_expense,
            "highest_expense": highest.amount if highest else 0.0
        }
    
    # ==================== SAVE FILE ====================
    
    def save_to_file(self):
        """
        Simpan semua transaksi ke file JSON
        Menelusuri DLL dan men-serialisasikan setiap node ke format kamus
        """
        transactions = []
        current = self.head
        
        # Traverse DLL and collect data
        while current:
            transactions.append(current.to_dict())
            current = current.next
        
        # Reverse to maintain chronological order in file
        transactions.reverse()
        
        data = {
            "transactions": transactions,
            "next_id": self.transaction_count + 1
        }
        
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_from_file(self):
        """
        Muat transaksi dari JSON dan melakukan rekonstruksi struktur data
        Membangun ulang DLL dan Max-Heap dari data yang disimpan
        Juga load recurring transactions ke queue
        """
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            self.transaction_count = data.get("next_id", 1) - 1
            transactions = data.get("transactions", [])
            
            # Reconstruct DLL (insert in reverse to maintain newest-first order)
            for trans in reversed(transactions):
                is_recurring = trans.get("is_recurring", False)
                recurrence_type = trans.get("recurrence_type", None)
                
                self.insert_at_head(
                    trans["date"],
                    trans["title"],
                    trans["amount"],
                    trans["type"],
                    trans["category"],
                    is_recurring,
                    recurrence_type
                )
        except Exception as e:
            print(f"Error loading data: {e}")