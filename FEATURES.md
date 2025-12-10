# FlowTrack - Fitur-Fitur Terbaru

Dokumentasi lengkap fitur-fitur yang ditambahkan untuk demo kepada professor.

## 1. 🔄 Edit Transaction (Update DLL)

### Deskripsi

Memungkinkan pengguna untuk mengedit transaksi yang sudah ada tanpa perlu menghapus dan menambah ulang. Ini menunjukkan operasi **UPDATE** pada **Doubly Linked List (DLL)**.

### Implementasi

- **File**: `models/finance_manager.py`
- **Method**: `update_node(node, date, title, amount, trans_type, category)`
- **Time Complexity**: O(1) untuk update field + O(n) jika ada perubahan amount (heap rebuild)

### Cara Penggunaan

1. Klik tombol **✎** pada setiap transaction card
2. Modal window akan terbuka dengan form untuk edit
3. Ubah field yang diperlukan
4. Klik **"Save Changes"** untuk menyimpan

### Demo Value

✅ Menunjukkan operasi **UPDATE pada DLL** (bukan delete-insert)
✅ Mempertahankan struktur DLL dan pointer-pointer
✅ Update statistics dan heap secara real-time

---

## 2. 📊 Export to CSV/Excel

### Deskripsi

Fitur untuk export semua transaksi ke file CSV yang bisa dibuka di Excel. Ini menunjukkan **TRAVERSAL pada DLL**.

### Implementasi

- **File**: `models/finance_manager.py`
- **Method**: `export_to_csv(filename)`
- **Time Complexity**: O(n) untuk traversal DLL

### Cara Penggunaan

1. Klik tombol **"📊 Export CSV"** di panel kiri
2. File akan di-generate dengan format `flowtrack_export_YYYYMMDD_HHMMSS.csv`
3. File akan disimpan di direktori project utama

### CSV Format

```
ID,Date,Title,Amount,Type,Category,Recurring,Recurrence Type
1,2024-12-10,Gaji,5000000,Income,Salary,No,-
2,2024-12-10,Makan,50000,Expense,Food,No,-
```

### Demo Value

✅ Menunjukkan **TRAVERSAL pada DLL** dari head ke tail
✅ Reverse order untuk chronological order
✅ Berguna untuk backup atau analisis eksternal di Excel

---

## 3. 💰 Monthly Budget Tracker (Binary Search Tree)

### Deskripsi

Fitur untuk menetapkan budget bulanan dan track spending. Menggunakan **Binary Search Tree (BST)** untuk menyimpan budget history per bulan.

### Implementasi

- **File**: `models/budget_bst.py`
- **Class**: `BudgetBST`, `BudgetNode`
- **Operations**:
  - `insert(month, budget_limit)` - O(log n) average
  - `search(month)` - O(log n) average
  - `delete(month)` - O(log n) average
  - `get_all_budgets()` - O(n) in-order traversal

### Fitur

- ✅ **Progress Bar**: Menunjukkan persentase spending vs budget
- ✅ **Status Alert**:
  - 🟢 Green jika masih aman
  - 🟠 Orange jika mendekati 80% limit
  - 🔴 Red jika over budget

### Cara Penggunaan

1. Masukkan amount di field "Budget Limit"
2. Klik tombol **"Set"**
3. Progress bar akan update otomatis saat ada transaksi baru

### BST Properties

- Key: Month string (YYYY-MM) - lexicographic = chronological order
- Value: BudgetNode berisi budget_limit dan spent amount
- In-order traversal menghasilkan history per bulan

### Demo Value

✅ Menunjukkan **Binary Search Tree operations**
✅ Insert, search, delete dengan balanced tree
✅ Range query untuk filter periode tertentu
✅ Real-time budget tracking

---

## 4. 🔄 Recurring Transactions (Queue Data Structure)

### Deskripsi

Menandai transaksi sebagai "recurring" (bulanan/mingguan) dan auto-add pada tanggal tertentu. Menggunakan **Queue** untuk menyimpan scheduled transactions.

### Implementasi

- **File**: `models/recurring_queue.py`
- **Class**: `RecurringTransactionQueue`, `ScheduledTransaction`
- **Data Structure**: Queue (FIFO) menggunakan Python list
  - `enqueue()` - O(1)
  - `dequeue()` - O(1) amortized
  - `peek()` - O(1)

### Cara Penggunaan

1. Saat membuat transaction, centang **"🔄 Recurring Transaction"**
2. Pilih tipe recurring: **"weekly"** atau **"monthly"**
3. Transaksi akan dijadwalkan ke queue

### Fitur

- ✅ **Weekly**: Repeat setiap minggunya
- ✅ **Monthly**: Repeat setiap bulannya
- ✅ **Badge**: Tampilkan 🔄 pada transaction card
- ✅ **Auto-scheduling**: Next date dihitung otomatis

### Queue Operations

```python
# Contoh penggunaan
queue = RecurringTransactionQueue()

# Enqueue transaction
scheduled = ScheduledTransaction(node, "2024-12-17")
queue.enqueue(scheduled)  # O(1)

# Dequeue transaction
trans = queue.dequeue()   # O(1)

# Get due transactions untuk tanggal tertentu
due_trans = queue.get_due_transactions("2024-12-17")  # O(n)
```

### Demo Value

✅ Menunjukkan **Queue Data Structure (FIFO)**
✅ Practical use case untuk scheduled payments
✅ Automatic date calculation untuk recurrence
✅ Traverse queue untuk process due transactions

---

## 5. 🎨 Enhanced UI Components

### Komponen Baru di `ui/components.py`

#### Progress Bar

```python
UIComponents.create_progress_bar(parent, value=0.5)
```

- Menampilkan persentase budget spending
- Support value 0.0-1.0, auto-clamp ke 1.0 jika over

#### Checkbox

```python
UIComponents.create_checkbox(parent, "Recurring Transaction", variable=var)
```

- Untuk toggle recurring transaction flag

#### Combobox

```python
UIComponents.create_combobox(parent, values=["weekly", "monthly"])
```

- Untuk memilih tipe recurrence

### Enhanced TransactionCard

- ✅ **Edit Button** (✎) - Buka modal untuk edit
- ✅ **Recurring Badge** (🔄) - Tampil jika transaksi recurring
- ✅ **Delete Button** (✕) - Hapus transaksi

---

## 6. Data Structure Summary

### Struktur Data yang Digunakan

| No  | Nama                   | File                 | Purpose                                         |
| --- | ---------------------- | -------------------- | ----------------------------------------------- |
| 1   | **DLL**                | `finance_manager.py` | Menyimpan transaksi dengan insert/update/delete |
| 2   | **Max-Heap**           | `max_heap.py`        | Tracking pengeluaran tertinggi                  |
| 3   | **Hash Map**           | `finance_manager.py` | Group transaksi by date                         |
| 4   | **Binary Search Tree** | `budget_bst.py`      | Budget history per bulan                        |
| 5   | **Queue**              | `recurring_queue.py` | Scheduled transactions                          |

### Complexity Analysis

```
Operation                Time Complexity      Space Complexity
─────────────────────────────────────────────────────────────
DLL Insert               O(1)                 O(1)
DLL Delete               O(1)                 O(1)
DLL Update               O(1)                 O(1)
DLL Search by ID         O(n)                 O(1)
DLL Traverse             O(n)                 O(1)
─────────────────────────────────────────────────────────────
Heap Insert              O(log n)             O(1)
Heap Get Max             O(1)                 O(1)
─────────────────────────────────────────────────────────────
Hash Map Insert          O(1) avg             O(n)
Hash Map Lookup          O(1) avg             O(1)
Hash Map Group by date   O(n)                 O(n)
─────────────────────────────────────────────────────────────
BST Insert               O(log n) avg         O(1)
BST Search               O(log n) avg         O(1)
BST Delete               O(log n) avg         O(1)
BST In-order Traverse    O(n)                 O(1)
─────────────────────────────────────────────────────────────
Queue Enqueue            O(1)                 O(1)
Queue Dequeue            O(1) amortized       O(1)
Queue Get Due Trans      O(n)                 O(k)
```

---

## 7. Demo Script untuk Professor

### Skenario Demo Lengkap

#### Demo 1: DLL UPDATE Operation (5 menit)

1. Buka aplikasi FlowTrack
2. Tambah beberapa transaksi (Income dan Expense)
3. Klik tombol Edit (✎) pada salah satu transaction
4. Ubah nilai amount/title
5. Klik Save → Perlihatkan update real-time tanpa delete-insert
6. Perlihatkan `finance_manager.py` → method `update_node()` → kompleksitas O(1)

#### Demo 2: DLL TRAVERSAL dengan Export CSV (3 menit)

1. Klik tombol "Export CSV"
2. Tunjukkan file CSV yang generated
3. Buka file di Excel → perlihatkan semua transaksi terurut
4. Perlihatkan code: traversal loop dari head ke tail

#### Demo 3: BST untuk Budget Tracking (5 menit)

1. Set budget untuk bulan ini (e.g., Rp 2.000.000)
2. Tambah expense yang mendekati budget
3. Perlihatkan progress bar update
4. Perlihatkan warning/alert saat mendekati/over limit
5. Perlihatkan BST structure: `budget_bst.py` → insert/search operations

#### Demo 4: Queue untuk Recurring Transactions (4 menit)

1. Buat recurring transaction (e.g., bulanan gaji)
2. Perlihatkan checkbox dan recurrence type selector
3. Perlihatkan badge (🔄) di transaction card
4. Perlihatkan `recurring_queue.py` → enqueue/dequeue operations
5. Jelaskan automatic scheduling logic

---

## 8. File-File Baru

```
models/
├── recurring_queue.py        [NEW] Queue untuk recurring transactions
└── budget_bst.py            [NEW] Binary Search Tree untuk budget

ui/
└── components.py            [UPDATED] Tambah progress_bar, checkbox, combobox

models/finance_manager.py    [UPDATED] Tambah update_node(), export_to_csv()
models/transaction_node.py   [UPDATED] Tambah is_recurring, recurrence_type fields
ui/main_window.py            [UPDATED] Tambah edit modal, budget section, recurring UI
```

---

## 9. Future Enhancements

- [ ] Persist recurring queue ke JSON
- [ ] Auto-process due recurring transactions
- [ ] Multiple budgets per bulan (e.g., kategori)
- [ ] Budget history chart/graph
- [ ] Email notifications untuk budget alerts
- [ ] Kategori management UI
- [ ] Transaction filtering dan searching

---

## 10. Technical Notes

### Circular Reference Prevention

- Import `Optional` dari `typing` untuk circular import prevention
- `RecurringTransactionQueue` dan `BudgetBST` tidak di-import langsung di `FinanceManager.__init__` class definition

### JSON Persistence

- Recurring fields disimpan ke JSON: `is_recurring`, `recurrence_type`
- Budget data bisa disimpan ke `data.json` di future

### Performance Considerations

- Heap rebuild O(n) hanya saat delete/update expense
- BST operations O(log n) untuk typical balanced tree
- CSV export O(n) untuk full traversal
- Queue operations mostly O(1) amortized

---

**Version**: 1.0  
**Last Updated**: December 2024  
**Author**: FlowTrack Development Team
