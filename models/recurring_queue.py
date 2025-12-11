from typing import Optional, List
from datetime import datetime, timedelta
from models.transaction_node import TransactionNode


class ScheduledTransaction:
    """
    Wrapper untuk scheduled transaction yang akan diproses nanti
    
    Attributes:
        node: Original TransactionNode
        next_due_date: Tanggal kapan transaksi recurring ini harus dijalankan
    """
    def __init__(self, node: TransactionNode, next_due_date: str):
        self.node = node
        self.next_due_date = next_due_date
    
    def __str__(self) -> str:
        return f"Scheduled: {self.node.title} on {self.next_due_date}"


class RecurringTransactionQueue:
    """
    Queue untuk menyimpan Scheduled Transactions yang akan diproses
    Menggunakan FIFO (First In First Out) principle
    
    Data Structure: Queue (menggunakan Python list dengan append/pop(0))
    - enqueue: O(1) - tambah ke belakang
    - dequeue: O(n) - ambil dari depan (tapi praktis O(1) untuk single item)
    - peek: O(1) - lihat item paling depan tanpa remove
    
    Good for Demo: Menunjukkan Queue data structure dan scheduling logic
    """
    
    def __init__(self):
        self.queue: List[ScheduledTransaction] = []
    
    def enqueue(self, scheduled_trans: ScheduledTransaction):
        """
        Tambahkan scheduled transaction ke queue
        
        Time Complexity: O(1)
        """
        self.queue.append(scheduled_trans)
    
    def dequeue(self) -> Optional[ScheduledTransaction]:
        """
        Ambil scheduled transaction dari depan queue (FIFO)
        
        Time Complexity: O(n) due to list pop(0), but practically O(1) for single item
        """
        if len(self.queue) > 0:
            return self.queue.pop(0)
        return None
    
    def peek(self) -> Optional[ScheduledTransaction]:
        """
        Lihat scheduled transaction di depan tanpa menghapusnya
        
        Time Complexity: O(1)
        """
        if len(self.queue) > 0:
            return self.queue[0]
        return None
    
    def is_empty(self) -> bool:
        """
        Check apakah queue kosong
        
        Time Complexity: O(1)
        """
        return len(self.queue) == 0
    
    def size(self) -> int:
        """
        Get ukuran queue
        
        Time Complexity: O(1)
        """
        return len(self.queue)
    
    def get_due_transactions(self, today: str) -> List[ScheduledTransaction]:
        """
        Dapatkan semua transaksi yang harus dijalankan pada tanggal tertentu
        
        Time Complexity: O(n) dimana n adalah ukuran queue
        
        Args:
            today: Current date in YYYY-MM-DD format
        
        Returns:
            List of ScheduledTransaction yang due date <= today
        """
        due = []
        i = 0
        while i < len(self.queue):
            if self.queue[i].next_due_date <= today:
                due.append(self.queue.pop(i))
            else:
                i += 1
        return due
    
    def schedule_recurring_transaction(self, node: TransactionNode, 
                                    start_date: str = None) -> None:
        """
        Schedule recurring transaction ke queue
        
        Args:
            node: TransactionNode dengan is_recurring=True
            start_date: Tanggal mulai (default: hari ini)
        """
        if not node.is_recurring or not node.recurrence_type:
            return
        
        start_date = start_date or datetime.now().strftime("%Y-%m-%d")
        next_date = self._calculate_next_date(start_date, node.recurrence_type)
        
        scheduled = ScheduledTransaction(node, next_date)
        self.enqueue(scheduled)
    
    @staticmethod
    def _calculate_next_date(current_date: str, recurrence_type: str) -> str:
        """
        Hitung tanggal berikutnya berdasarkan tipe recurrence
        
        Args:
            current_date: Tanggal saat ini (YYYY-MM-DD)
            recurrence_type: "monthly" atau "weekly"
        
        Returns:
            Tanggal berikutnya dalam format YYYY-MM-DD
        """
        date_obj = datetime.strptime(current_date, "%Y-%m-%d")
        
        if recurrence_type == "weekly":
            next_date = date_obj + timedelta(weeks=1)
        elif recurrence_type == "monthly":
            # Tambah 1 bulan (handle end of month dengan hati-hati)
            if date_obj.month == 12:
                next_date = date_obj.replace(year=date_obj.year + 1, month=1)
            else:
                next_date = date_obj.replace(month=date_obj.month + 1)
        else:
            next_date = date_obj
        
        return next_date.strftime("%Y-%m-%d")
    
    def __str__(self) -> str:
        """Representation string"""
        return f"RecurringQueue[{len(self.queue)} scheduled transactions]"
