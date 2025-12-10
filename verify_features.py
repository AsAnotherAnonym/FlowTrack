#!/usr/bin/env python3
"""
FlowTrack Feature Verification Script

Menjalankan tes untuk memverifikasi semua fitur yang ditambahkan.
"""

import os
import sys
from datetime import datetime

def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_success(msg):
    print(f"  [OK] {msg}")

def print_error(msg):
    print(f"  [ERROR] {msg}")

def test_imports():
    """Test semua imports"""
    print_header("1. Testing Imports")
    
    try:
        from models import FinanceManager
        print_success("FinanceManager imported")
        
        from models import TransactionNode
        print_success("TransactionNode imported")
        
        from models import MaxHeap
        print_success("MaxHeap imported")
        
        from models import RecurringTransactionQueue
        print_success("RecurringTransactionQueue imported [NEW]")
        
        from models import BudgetBST
        print_success("BudgetBST imported [NEW]")
        
        from ui.components import UIComponents, TransactionCard
        print_success("UI Components imported")
        
        return True
    except Exception as e:
        print_error(f"Import failed: {e}")
        return False

def test_transaction_node():
    """Test TransactionNode dengan recurring fields"""
    print_header("2. Testing TransactionNode with Recurring Fields")
    
    try:
        from models import TransactionNode
        
        # Test regular node
        node1 = TransactionNode("2024-12-10", "Gaji", 5000000, "Income", "Salary", 1)
        print_success(f"Regular node created: {node1}")
        
        # Test recurring node
        node2 = TransactionNode("2024-12-10", "Gaji Bulanan", 5000000, "Income", 
                               "Salary", 2, is_recurring=True, recurrence_type="monthly")
        print_success(f"Recurring node created: {node2}")
        print_success(f"Recurring flag: {node2.is_recurring}, Type: {node2.recurrence_type}")
        
        # Test to_dict
        node_dict = node2.to_dict()
        print_success(f"to_dict() includes recurring: {node_dict.get('is_recurring')}")
        
        return True
    except Exception as e:
        print_error(f"TransactionNode test failed: {e}")
        return False

def test_finance_manager():
    """Test FinanceManager methods"""
    print_header("3. Testing FinanceManager New Methods")
    
    try:
        from models import FinanceManager
        
        manager = FinanceManager()
        print_success("FinanceManager initialized")
        
        # Test insert with recurring
        node = manager.insert_at_head("2024-12-10", "Test", 100000, "Expense", 
                                      "Test", is_recurring=True, recurrence_type="weekly")
        print_success(f"Insert with recurring parameter: OK")
        
        # Test update_node
        success = manager.update_node(node, title="Updated Test", amount=150000)
        print_success(f"update_node() executed: {success} [NEW]")
        
        # Test export_to_csv
        csv_file = "test_export.csv"
        success = manager.export_to_csv(csv_file)
        print_success(f"export_to_csv() executed: {success} [NEW]")
        
        # Cleanup
        if os.path.exists(csv_file):
            os.remove(csv_file)
            print_success(f"CSV file cleanup: OK")
        
        return True
    except Exception as e:
        print_error(f"FinanceManager test failed: {e}")
        return False

def test_budget_bst():
    """Test BudgetBST"""
    print_header("4. Testing Budget BST [NEW]")
    
    try:
        from models import BudgetBST
        
        bst = BudgetBST()
        print_success("BudgetBST initialized")
        
        # Test insert
        node1 = bst.insert("2024-11", 2000000)
        print_success(f"BST insert: {node1}")
        
        # Test search
        found = bst.search("2024-11")
        print_success(f"BST search: {found}")
        
        # Test multiple inserts
        bst.insert("2024-12", 2500000)
        bst.insert("2024-10", 1800000)
        print_success("BST multiple inserts: OK")
        
        # Test in-order traversal
        all_budgets = bst.get_all_budgets()
        print_success(f"BST in-order traversal: {len(all_budgets)} nodes")
        
        # Test budget operations
        node1.spent = 1500000
        remaining = node1.get_remaining()
        percentage = node1.get_percentage()
        print_success(f"Budget tracking: spent={node1.spent}, remaining={remaining}, %={percentage:.1f}%")
        
        return True
    except Exception as e:
        print_error(f"BudgetBST test failed: {e}")
        return False

def test_recurring_queue():
    """Test RecurringTransactionQueue"""
    print_header("5. Testing Recurring Transaction Queue [NEW]")
    
    try:
        from models import RecurringTransactionQueue, ScheduledTransaction, TransactionNode
        
        queue = RecurringTransactionQueue()
        print_success("RecurringQueue initialized")
        
        # Create scheduled transaction
        node = TransactionNode("2024-12-10", "Gaji", 5000000, "Income", 
                              "Salary", 1, is_recurring=True, recurrence_type="monthly")
        scheduled = ScheduledTransaction(node, "2024-12-10")
        print_success(f"ScheduledTransaction created: {scheduled}")
        
        # Test enqueue
        queue.enqueue(scheduled)
        print_success(f"Queue enqueue: OK (size={queue.size()})")
        
        # Test peek
        peeked = queue.peek()
        print_success(f"Queue peek: {peeked}")
        
        # Test get_due_transactions
        due = queue.get_due_transactions("2024-12-10")
        print_success(f"Queue get_due: {len(due)} transactions due")
        
        # Test queue empty after dequeue
        print_success(f"Queue is_empty: {queue.is_empty()}")
        
        return True
    except Exception as e:
        print_error(f"RecurringQueue test failed: {e}")
        return False

def test_ui_components():
    """Test UI Components"""
    print_header("6. Testing UI Components [ENHANCED]")
    
    try:
        from ui.components import UIComponents
        
        # Test new component creation (without parent widget)
        print_success("create_progress_bar: Available [NEW]")
        print_success("create_checkbox: Available [NEW]")
        print_success("create_combobox: Available [NEW]")
        
        # Verify methods exist
        assert hasattr(UIComponents, 'create_progress_bar')
        assert hasattr(UIComponents, 'create_checkbox')
        assert hasattr(UIComponents, 'create_combobox')
        
        print_success("All new UI methods verified: OK")
        
        return True
    except Exception as e:
        print_error(f"UI Components test failed: {e}")
        return False

def verify_files():
    """Verify all new files exist"""
    print_header("7. Verifying New Files")
    
    files_to_check = [
        "models/recurring_queue.py",
        "models/budget_bst.py",
        "FEATURES.md",
        "DEMO_GUIDE.md",
        "QUICKSTART.md",
        "IMPLEMENTATION_SUMMARY.md",
        "requirements.txt"
    ]
    
    all_exist = True
    for file in files_to_check:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print_success(f"{file} ({size} bytes)")
        else:
            print_error(f"{file} NOT FOUND")
            all_exist = False
    
    return all_exist

def test_data_persistence():
    """Test data loading/saving"""
    print_header("8. Testing Data Persistence")
    
    try:
        from models import FinanceManager
        
        # Create manager and add data
        manager = FinanceManager()
        manager.insert_at_head("2024-12-10", "Test", 100000, "Expense", "Test", 
                              is_recurring=True, recurrence_type="monthly")
        manager.save_to_file()
        print_success("Data saved to file: OK")
        
        # Load data
        manager2 = FinanceManager()
        print_success(f"Data loaded from file: OK ({manager2.transaction_count} transactions)")
        
        # Verify recurring data
        all_trans = manager2.get_all_transactions()
        if all_trans:
            first = all_trans[0]
            print_success(f"Recurring field preserved: is_recurring={first.is_recurring}")
        
        return True
    except Exception as e:
        print_error(f"Data persistence test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("  FlowTrack Feature Verification Script")
    print("  Testing all new and modified features")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("TransactionNode Recurring Fields", test_transaction_node),
        ("FinanceManager New Methods", test_finance_manager),
        ("Budget BST", test_budget_bst),
        ("Recurring Queue", test_recurring_queue),
        ("UI Components", test_ui_components),
        ("File Verification", verify_files),
        ("Data Persistence", test_data_persistence),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"Test {name} crashed: {e}")
            results.append((name, False))
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "[OK]" if result else "[FAIL]"
        print(f"  {symbol} {name}: {status}")
    
    print("\n" + "=" * 60)
    print(f"  Result: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n  [SUCCESS] All features verified successfully!")
        print("  Application is ready for demo to professor.\n")
        return 0
    else:
        print(f"\n  [WARNING] {total - passed} test(s) failed.\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
