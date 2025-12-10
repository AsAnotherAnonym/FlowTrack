# FlowTrack - Demo Guide untuk Professor

Panduan step-by-step untuk demo semua fitur kepada professor.

## 📋 Checklist Sebelum Demo

- [ ] Aplikasi sudah di-test dan berjalan normal
- [ ] Data transactions sudah disiapkan
- [ ] File `FEATURES.md` siap untuk referensi
- [ ] Terminal/PowerShell siap untuk buka file source code
- [ ] VS Code siap dengan file-file terbuka

---

## 🎬 Demo Flow (Total ~20 menit)

### 1️⃣ INTRODUCTION (1 menit)

**Apa itu FlowTrack?**

- Personal Finance Manager dengan multiple data structures
- Menunjukkan implementasi praktis struktur data dalam aplikasi real-world
- Menggunakan DLL, Max-Heap, Hash Map, BST, dan Queue

**Struktur Data yang Digunakan:**
| Data Structure | Use Case |
|---|---|
| Doubly Linked List | Menyimpan transaksi |
| Max-Heap | Track pengeluaran tertinggi |
| Hash Map | Group transaksi by date |
| Binary Search Tree | Budget history per bulan |
| Queue | Scheduled recurring transactions |

---

### 2️⃣ DEMO 1: DOUBLY LINKED LIST - INSERT & DELETE (3 menit)

**Target**: Perlihatkan operasi INSERT dan DELETE pada DLL

**Steps:**

1. **Open Application**

   ```bash
   cd d:\strukdat\FlowTrack
   & "D:/strukdat/FlowTrack/.venv/Scripts/python.exe" main.py
   ```

2. **Add Transactions**

   - Tambah transaksi pertama: "Gaji Bulanan" - Rp 5,000,000 (Income)
   - Tambah transaksi kedua: "Makan Siang" - Rp 50,000 (Expense)
   - Tambah transaksi ketiga: "Belanja Groceries" - Rp 200,000 (Expense)
   - Perhatikan: Transaksi terbaru muncul di paling atas (insert at head)

3. **Show Code Structure**

   ```python
   # Buka: models/transaction_node.py
   # Perlihatkan:
   # - self.next: pointer ke node berikutnya
   # - self.prev: pointer ke node sebelumnya
   ```

4. **Delete Transaction**

   - Klik tombol ✕ pada salah satu transaksi
   - Perlihatkan: Node dihapus, pointer-pointer di-update

5. **Key Points:**
   - ✅ Insert at head: O(1) - tidak perlu traverse
   - ✅ Delete: O(1) - cukup update pointer
   - ✅ Newest first order: Untuk UX yang lebih baik

---

### 3️⃣ DEMO 2: DLL UPDATE - EDIT TRANSACTION (3 menit)

**Target**: Perlihatkan operasi UPDATE pada DLL (bukan delete-insert)

**Steps:**

1. **Open Edit Modal**

   - Klik tombol ✎ pada salah satu transaction card
   - Modal window akan terbuka dengan pre-filled data

2. **Edit Transaction**

   - Ubah Title: "Makan Siang" → "Makan Siang Premium"
   - Ubah Amount: "50,000" → "100,000"
   - Klik "Save Changes"

3. **Show Real-time Update**

   - ✅ Statistics update (total expense bertambah)
   - ✅ Max-Heap rebuild untuk highest expense
   - ✅ Budget progress update otomatis
   - ✅ Tidak ada re-creation node, hanya in-place update

4. **Show Code**

   ```python
   # Buka: models/finance_manager.py
   # Perlihatkan method: update_node()

   # Kompleksitas:
   # - Field update: O(1)
   # - Statistics update: O(1)
   # - Heap rebuild (if expense): O(n)
   ```

5. **Key Points:**
   - ✅ UPDATE operation: O(1) untuk field update
   - ✅ Struktur DLL tetap intact, pointer tidak berubah
   - ✅ Lebih efisien daripada delete-insert (O(1) vs O(2))
   - ✅ Transaction tetap pada posisi yang sama di list

---

### 4️⃣ DEMO 3: DLL TRAVERSAL - EXPORT CSV (2 menit)

**Target**: Perlihatkan traversal pada DLL dan export ke CSV

**Steps:**

1. **Click Export Button**

   - Klik tombol "📊 Export CSV" di panel kiri
   - File akan di-generate: `flowtrack_export_YYYYMMDD_HHMMSS.csv`

2. **Show Generated File**

   ```bash
   # Di PowerShell:
   ls *.csv  # Lihat file yang baru dibuat
   cat flowtrack_export_*.csv  # Tampilkan isi file
   ```

3. **Open in Excel** (Optional)

   ```bash
   # Buka di Excel untuk perlihatkan format yang rapi
   Invoke-Item (ls *.csv | Select-Object -First 1)
   ```

4. **Show Code - Traversal Logic**

   ```python
   # Buka: models/finance_manager.py
   # Method: export_to_csv()

   # Perlihatkan:
   current = self.head
   while current:
       transactions.append(current.to_dict())
       current = current.next  # Traverse ke node berikutnya
   ```

5. **Key Points:**
   - ✅ TRAVERSAL: O(n) dari head ke tail
   - ✅ Dalam-order (newest first) di aplikasi, reversed untuk chronological
   - ✅ Reverse list: transactions.reverse()
   - ✅ CSV format: Comma-separated values untuk interoperability

---

### 5️⃣ DEMO 4: MAX-HEAP - HIGHEST EXPENSE (2 menit)

**Target**: Perlihatkan Max-Heap untuk tracking highest expense

**Steps:**

1. **Show Highest Expense Section**

   - Di panel kiri, section "🔥 Highest Expense (Max-Heap)"
   - Perlihatkan transaksi dengan amount terbesar

2. **Observe Auto-Update**

   - Tambah expense baru yang lebih besar
   - Highest expense akan update otomatis
   - Atau hapus highest expense → lihat update ke yang kedua terbesar

3. **Show Max-Heap Properties**

   ```python
   # Buka: models/max_heap.py

   # Perlihatkan:
   # - Parent index: i // 2
   # - Left child: 2*i + 1
   # - Right child: 2*i + 2
   # - Max element selalu di root (index 0)
   ```

4. **Key Points:**
   - ✅ GET MAX: O(1) - element terbesar selalu di root
   - ✅ INSERT: O(log n) - bubble up operation
   - ✅ Heap rebuild saat delete expense: O(n)
   - ✅ Trade-off: Cepat untuk read, update memerlukan rebuild

---

### 6️⃣ DEMO 5: HASH MAP - GROUP BY DATE (1 menit)

**Target**: Perlihatkan hash map untuk grouping transaksi

**Steps:**

1. **Look at Transaction List**

   - Transaksi dikelompokkan berdasarkan tanggal
   - Header tanggal di atas setiap grup

2. **Show Hash Map Implementation**

   ```python
   # Buka: models/finance_manager.py
   # Method: group_by_date()

   date_map: Dict[str, List[TransactionNode]] = {}
   # Key: "2024-12-10"
   # Value: List of all transactions pada tanggal tersebut
   ```

3. **Key Points:**
   - ✅ GROUP: O(n) untuk traverse semua transaksi
   - ✅ LOOKUP: O(1) untuk get transaksi di tanggal tertentu
   - ✅ Efficient untuk date-based queries

---

### 7️⃣ DEMO 6: BINARY SEARCH TREE - BUDGET TRACKING (3 menit)

**Target**: Perlihatkan BST untuk budget history per bulan

**Steps:**

1. **Set Budget**

   - Di section "💰 Monthly Budget"
   - Masukkan budget: "2000000"
   - Klik tombol "Set"

2. **See Progress Bar**

   - Progress bar akan menunjukkan: 0% (tidak ada spending yet)
   - Perlihatkan status text: "✓ Rp 2,000,000 remaining (0%)"

3. **Add Expenses**

   - Tambah beberapa expense
   - Perlihatkan progress bar update real-time
   - Progress bar berubah warna:
     - 🟢 Green: Safe (< 80%)
     - 🟠 Orange: Warning (80-100%)
     - 🔴 Red: Over budget (> 100%)

4. **Show Budget Alerts**

   - Terus tambah expense sampai mendekati/melebihi budget
   - Perlihatkan:
     - "⚡ Near limit: Rp XX remaining (80%)"
     - "⚠️ Over budget by Rp XX"

5. **Show BST Code Structure**

   ```python
   # Buka: models/budget_bst.py

   # Perlihatkan:
   # - BudgetNode: month (key), budget_limit, spent
   # - Binary Search Tree:
   #   - insert(): O(log n) avg
   #   - search(): O(log n) avg
   #   - In-order traversal: O(n) → chronological order

   # Key: Month string "2024-12" (lexicographic = chronological)
   ```

6. **Key Points:**
   - ✅ BST INSERT: O(log n) average case
   - ✅ BST SEARCH: O(log n) untuk find budget bulan tertentu
   - ✅ IN-ORDER TRAVERSAL: O(n) → history chronological
   - ✅ Range query: Bisa get budgets antara dua periode
   - ✅ Real-time tracking: Update spent saat ada expense baru

---

### 8️⃣ DEMO 7: QUEUE - RECURRING TRANSACTIONS (3 menit)

**Target**: Perlihatkan Queue untuk scheduled recurring transactions

**Steps:**

1. **Create Recurring Transaction**

   - Tambah transaksi baru
   - Centang checkbox: "🔄 Recurring Transaction"
   - Pilih: "monthly" (dari combobox)
   - Tambahkan transaksi: "Bayar Internet" - Rp 100,000

2. **See Recurring Badge**

   - Di transaction card, perlihatkan badge: "🔄 monthly"
   - Badge ini menunjukkan transaksi adalah recurring

3. **Show Queue Implementation**

   ```python
   # Buka: models/recurring_queue.py

   # Class: RecurringTransactionQueue
   # - enqueue(): O(1) - tambah ke belakang queue
   # - dequeue(): O(1) amortized - ambil dari depan
   # - peek(): O(1) - lihat element di depan tanpa remove
   # - get_due_transactions(): O(n) - cari transaksi yang due
   ```

4. **Show Scheduling Logic**

   ```python
   # Buka: models/recurring_queue.py
   # Method: _calculate_next_date()

   # Jika monthly: date + 1 bulan
   # Jika weekly: date + 1 minggu
   # Handle edge cases: end of month, year boundary
   ```

5. **Explain Use Case**

   - Gaji bulanan: automatically scheduled
   - Langganan bulanan: automatically added
   - Future feature: auto-process due transactions

6. **Key Points:**
   - ✅ QUEUE: FIFO data structure (First In First Out)
   - ✅ ENQUEUE: O(1) - scheduling transaksi
   - ✅ DEQUEUE: O(1) amortized
   - ✅ Practical use case: recurring payments
   - ✅ Automatic date calculation: flexible recurrence logic

---

### 9️⃣ SUMMARY & Q&A (2 menit)

**Ringkasan Data Structures:**

```
┌─────────────────────────────────────────────────────────┐
│              FLOWTRACK DATA STRUCTURES                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 1. DOUBLY LINKED LIST (DLL)                            │
│    ├─ Insert: O(1)     [Newest transactions at head]   │
│    ├─ Delete: O(1)     [Remove dari linked list]       │
│    └─ Update: O(1)     [NEW! In-place modification]    │
│                                                         │
│ 2. MAX-HEAP                                            │
│    ├─ Insert: O(log n) [Track highest expense]         │
│    └─ Get Max: O(1)    [Access max element]            │
│                                                         │
│ 3. HASH MAP (Dictionary)                               │
│    ├─ Insert: O(1)     [Group by date]                 │
│    └─ Lookup: O(1)     [Get transactions for date]     │
│                                                         │
│ 4. BINARY SEARCH TREE                                  │
│    ├─ Insert: O(log n) [Monthly budget]                │
│    ├─ Search: O(log n) [Find budget for month]         │
│    └─ Traverse: O(n)   [History chronological]         │
│                                                         │
│ 5. QUEUE (FIFO)                                        │
│    ├─ Enqueue: O(1)    [Schedule recurring trans]      │
│    └─ Dequeue: O(1)    [Process due transactions]      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Features Implemented:**

| Feature      | Fitur             | Data Structure | Demo Value            |
| ------------ | ----------------- | -------------- | --------------------- |
| ✎ Edit       | In-place update   | DLL            | O(1) UPDATE operation |
| 📊 Export    | CSV export        | DLL            | O(n) TRAVERSAL        |
| 💰 Budget    | Monthly tracking  | BST            | O(log n) operations   |
| 🔄 Recurring | Schedule payments | Queue          | FIFO scheduling       |

**Questions untuk Interaksi dengan Professor:**

- "Bagaimana struktur DLL membantu untuk operasi insert/delete?"
- "Kenapa Max-Heap lebih efisien untuk tracking highest expense?"
- "Bagaimana BST memastikan budget history tetap sorted?"
- "Apa keuntungan menggunakan Queue untuk recurring transactions?"
- "Bagaimana jika ada banyak transaksi? Apakah struktur data ini scalable?"

---

## 🛠️ Technical Deep Dive (Untuk Pertanyaan Lanjutan)

### Time Complexity Analysis

**Worst Case vs Average Case:**

```
DLL Operations:
- Best/Avg/Worst Insert at head: O(1)
- Best/Avg/Worst Delete: O(1)
- Best/Avg/Worst Update: O(1)
- Traversal: O(n)

BST Operations:
- Balanced tree:    O(log n) avg
- Skewed tree:      O(n) worst
- Traversal:        O(n)

Heap Operations:
- Insert:           O(log n)
- Get Max:          O(1)
- Delete Max:       O(log n)

Queue Operations:
- Enqueue/Dequeue:  O(1)
- Peek:             O(1)
```

### Space Complexity

```
DLL:     O(n) - setiap node occupies memory
Heap:    O(n) - array-based representation
BST:     O(n) - worst case skewed tree
Queue:   O(n) - list-based representation
HashMap: O(n) - bucket + entries
```

### Comparison dengan Alternatif

**Untuk menyimpan transaksi:**

- Array: Insert/Delete O(n) ❌
- Linked List: Insert/Delete O(n) jika search, O(1) jika tahu lokasi ✅
- **DLL**: Insert at head O(1), Delete O(1) jika punya reference ✅✅

**Untuk tracking highest expense:**

- Linear scan setiap query: O(n) ❌
- **Max-Heap**: Get O(1), Insert O(log n) ✅✅

**Untuk grouping by date:**

- Linear search: O(n) ❌
- **Hash Map**: O(1) lookup ✅✅

---

## 📝 Tips untuk Demo

1. **Practice Beforehand**

   - Jalankan demo di komputer sendiri 2-3 kali
   - Pastikan timing sesuai (~20 menit)

2. **Show Code di Proper Order**

   - Transaction node definition
   - DLL operations (insert/delete/update)
   - Traversal logic
   - Data structure classes

3. **Use Real Data**

   - Gunakan transaksi dengan nominal realistic
   - Buat budget scenario yang relatable
   - Recurring transaction contoh yang umum (gaji, langganan)

4. **Interactive Demo**

   - Tanyakan pertanyaan ke professor: "Apa kompleksitas operasi ini?"
   - Minta saran: "Bagaimana kalau kita pakai struktur data lain?"
   - Diskusikan trade-off: "Kenapa pilih DLL daripada array?"

5. **Backup Plan**
   - Screenshot fitur sudah siap jika aplikasi crash
   - Code printout untuk referensi
   - Pre-recorded video sebagai backup terakhir

---

## 🎓 Learning Outcomes untuk Professor

Setelah demo ini, professor akan melihat:

✅ **Practical Implementation**

- Struktur data bukan hanya teori, tapi untuk real-world app

✅ **Performance Consideration**

- Pemilihan data structure berpengaruh pada performance

✅ **Trade-offs**

- Setiap struktur data punya kelebihan dan kekurangan

✅ **Integration**

- Bagaimana multiple data structure bekerja bersama

✅ **Problem Solving**

- Bagaimana design solution dari requirement

---

**Good luck with your demo! 🚀**
