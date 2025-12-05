from models.transaction_node import TransactionNode
from typing import List, Optional, Tuple

class MaxHeap:
    """
    Implementasi Max-Heap untuk melacak pengeluaran tertinggi
    
    Heap ini menyimpan pengeluaran tertinggi di akar/root, memungkinkan akses O(1)
    ke pengeluaran tertinggi dan insertion O(log n).
    
    Time Complexities:
        - insert(): O(log n)
        - get_max(): O(1)
        - rebuild_from_dll(): O(n)
    
    Attributes:
        heap: List of tuples (amount, node) where amount is the key
    """
    
    def __init__(self):
        self.heap: List[Tuple[float, TransactionNode]] = []
    
    def _parent(self, i: int) -> int:
        """Get parent index"""
        return (i - 1) // 2
    
    def _left_child(self, i: int) -> int:
        """Get left child index"""
        return 2 * i + 1
    
    def _right_child(self, i: int) -> int:
        """Get right child index"""
        return 2 * i + 2
    
    def _swap(self, i: int, j: int):
        """Swap two elements in the heap"""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def _heapify_up(self, i: int):
        """
        Mempertahankan sifat max-heap dengan memindahkan elemen ke atas
        Digunakan setelah insertion
        """
        while i > 0:
            parent = self._parent(i)
            if self.heap[i][0] > self.heap[parent][0]:
                self._swap(i, parent)
                i = parent
            else:
                break
    
    def _heapify_down(self, i: int):
        """
        Mempertahankan sifat max-heap dengan memindahkan elemen ke bawah
        Digunakan selama proses rebuild heap
        """
        size = len(self.heap)
        while True:
            largest = i
            left = self._left_child(i)
            right = self._right_child(i)
            
            if left < size and self.heap[left][0] > self.heap[largest][0]:
                largest = left
            if right < size and self.heap[right][0] > self.heap[largest][0]:
                largest = right
            
            if largest != i:
                self._swap(i, largest)
                i = largest
            else:
                break
    
    def insert(self, amount: float, node: TransactionNode):
        """
        Memasukkan pengeluaran ke dalam heap
        Time Complexity: O(log n)
        
        Args:
            amount: The expense amount (heap key)
            node: The transaction node reference
        """
        self.heap.append((amount, node))
        self._heapify_up(len(self.heap) - 1)
    
    def get_max(self) -> Optional[TransactionNode]:
        """
        Mencari pengeluaran tertinggi tanpa menghapusnya
        Time Complexity: O(1)
        
        Returns:
            TransactionNode with highest expense, or None if heap is empty
        """
        return self.heap[0][1] if self.heap else None
    
    def rebuild_from_dll(self, head: Optional[TransactionNode]):
        """
        Membuat ulang heap dari semua transaksi pengeluaran dalam DLL
        Time Complexity: O(n)
        
        Dinamakan saat pengeluaran dihapus untuk menjaga integritas heap.
        
        Args:
            head: Head of the doubly linked list
        """
        self.heap = []
        current = head
        
        # Collect all expense transactions
        while current:
            if current.trans_type == "Expense":
                self.heap.append((current.amount, current))
            current = current.next
        
        # Build heap from bottom up (Floyd's algorithm)
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self._heapify_down(i)
    
    def size(self) -> int:
        """Return jumlah element dari dalam heap"""
        return len(self.heap)
    
    def is_empty(self) -> bool:
        """Mengecek apakah heap kosong"""
        return len(self.heap) == 0