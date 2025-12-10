from typing import Optional


class BudgetNode:
    """
    Node untuk Binary Search Tree yang menyimpan budget history per bulan
    
    Attributes:
        month: Bulan dalam format YYYY-MM (e.g., "2024-12")
        budget_limit: Budget amount untuk bulan tersebut
        spent: Total pengeluaran untuk bulan tersebut
        left: Left child node
        right: Right child node
    """
    def __init__(self, month: str, budget_limit: float):
        self.month = month
        self.budget_limit = budget_limit
        self.spent = 0.0
        self.left: Optional[BudgetNode] = None
        self.right: Optional[BudgetNode] = None
    
    def get_remaining(self) -> float:
        """Get sisa budget"""
        return self.budget_limit - self.spent
    
    def get_percentage(self) -> float:
        """Get persentase budget yang sudah digunakan (0-100)"""
        if self.budget_limit == 0:
            return 0
        return (self.spent / self.budget_limit) * 100
    
    def is_over_budget(self) -> bool:
        """Check apakah sudah melebihi budget"""
        return self.spent > self.budget_limit
    
    def is_near_limit(self, threshold: float = 80.0) -> bool:
        """Check apakah mendekati limit (default: 80%)"""
        return self.get_percentage() >= threshold
    
    def __str__(self) -> str:
        return f"Budget({self.month}): {self.spent}/{self.budget_limit}"


class BudgetBST:
    """
    Binary Search Tree untuk menyimpan Budget history per bulan
    Menggunakan bulan sebagai key untuk sorting (lexicographic order = chronological)
    
    Data Structure: Binary Search Tree (BST)
    - insert: O(log n) average, O(n) worst case
    - search: O(log n) average, O(n) worst case
    - delete: O(log n) average, O(n) worst case
    - in-order traversal: O(n)
    
    Good for Demo: Menunjukkan BST data structure dan operations
    """
    
    def __init__(self):
        self.root: Optional[BudgetNode] = None
    
    def insert(self, month: str, budget_limit: float) -> BudgetNode:
        """
        Insert atau update budget untuk bulan tertentu
        Jika sudah ada, return node yang ada; jika belum, buat baru
        
        Time Complexity: O(log n) average, O(n) worst case
        
        Args:
            month: Bulan dalam format YYYY-MM
            budget_limit: Budget amount untuk bulan tersebut
        
        Returns:
            The BudgetNode (baru atau existing)
        """
        if self.root is None:
            self.root = BudgetNode(month, budget_limit)
            return self.root
        
        return self._insert_recursive(self.root, month, budget_limit)
    
    def _insert_recursive(self, node: Optional[BudgetNode], 
                         month: str, budget_limit: float) -> BudgetNode:
        """Helper untuk recursive insertion"""
        if node is None:
            return BudgetNode(month, budget_limit)
        
        if month < node.month:
            node.left = self._insert_recursive(node.left, month, budget_limit)
        elif month > node.month:
            node.right = self._insert_recursive(node.right, month, budget_limit)
        else:
            # Node dengan bulan yang sama, update saja
            node.budget_limit = budget_limit
        
        return node
    
    def search(self, month: str) -> Optional[BudgetNode]:
        """
        Cari budget untuk bulan tertentu
        
        Time Complexity: O(log n) average, O(n) worst case
        
        Args:
            month: Bulan dalam format YYYY-MM
        
        Returns:
            BudgetNode if found, None otherwise
        """
        return self._search_recursive(self.root, month)
    
    def _search_recursive(self, node: Optional[BudgetNode], month: str) -> Optional[BudgetNode]:
        """Helper untuk recursive search"""
        if node is None:
            return None
        
        if month < node.month:
            return self._search_recursive(node.left, month)
        elif month > node.month:
            return self._search_recursive(node.right, month)
        else:
            return node
    
    def delete(self, month: str) -> bool:
        """
        Delete budget untuk bulan tertentu
        
        Time Complexity: O(log n) average, O(n) worst case
        
        Args:
            month: Bulan dalam format YYYY-MM
        
        Returns:
            True if deletion was successful, False otherwise
        """
        self.root, deleted = self._delete_recursive(self.root, month)
        return deleted
    
    def _delete_recursive(self, node: Optional[BudgetNode], 
                         month: str) -> tuple:
        """Helper untuk recursive deletion, return (new_node, was_deleted)"""
        if node is None:
            return None, False
        
        if month < node.month:
            node.left, deleted = self._delete_recursive(node.left, month)
            return node, deleted
        elif month > node.month:
            node.right, deleted = self._delete_recursive(node.right, month)
            return node, deleted
        else:
            # Node ditemukan, hapus
            # Case 1: No children (leaf node)
            if node.left is None and node.right is None:
                return None, True
            
            # Case 2: One child
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True
            
            # Case 3: Two children
            # Find in-order successor (smallest in right subtree)
            successor = self._find_min(node.right)
            node.month = successor.month
            node.budget_limit = successor.budget_limit
            node.spent = successor.spent
            node.right, _ = self._delete_recursive(node.right, successor.month)
            return node, True
    
    def _find_min(self, node: BudgetNode) -> BudgetNode:
        """Find node dengan nilai minimum (paling kiri)"""
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def get_all_budgets(self) -> list:
        """
        Get semua budget dalam urutan chronological (in-order traversal)
        
        Time Complexity: O(n)
        
        Returns:
            List of BudgetNode in sorted order
        """
        result = []
        self._in_order_traversal(self.root, result)
        return result
    
    def _in_order_traversal(self, node: Optional[BudgetNode], result: list):
        """Helper untuk in-order traversal"""
        if node is not None:
            self._in_order_traversal(node.left, result)
            result.append(node)
            self._in_order_traversal(node.right, result)
    
    def get_budgets_in_range(self, start_month: str, end_month: str) -> list:
        """
        Get budgets dalam range tertentu (untuk filter/view)
        
        Time Complexity: O(k + log n) dimana k adalah jumlah hasil
        
        Args:
            start_month: Awal range (YYYY-MM)
            end_month: Akhir range (YYYY-MM)
        
        Returns:
            List of BudgetNode dalam range
        """
        result = []
        self._range_search(self.root, start_month, end_month, result)
        return result
    
    def _range_search(self, node: Optional[BudgetNode], 
                     start_month: str, end_month: str, result: list):
        """Helper untuk range search"""
        if node is None:
            return
        
        if node.month >= start_month:
            self._range_search(node.left, start_month, end_month, result)
        
        if start_month <= node.month <= end_month:
            result.append(node)
        
        if node.month <= end_month:
            self._range_search(node.right, start_month, end_month, result)
    
    def get_current_month_budget(self, current_month: str) -> Optional[BudgetNode]:
        """
        Get budget untuk bulan saat ini (convenience method)
        
        Args:
            current_month: Bulan saat ini (YYYY-MM)
        
        Returns:
            BudgetNode or None
        """
        return self.search(current_month)
    
    def update_spending(self, month: str, amount: float):
        """
        Update spending untuk bulan tertentu
        
        Args:
            month: Bulan (YYYY-MM)
            amount: Jumlah yang dihabiskan untuk ditambahkan
        """
        node = self.search(month)
        if node:
            node.spent += amount
    
    def __str__(self) -> str:
        """Representation string"""
        budgets = self.get_all_budgets()
        return f"BudgetBST[{len(budgets)} months]"
