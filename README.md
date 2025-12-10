# FlowTrack - Manajer Keuangan Pribadi

Aplikasi manajer keuangan pribadi modern yang dibangun dengan Python dan CustomTkinter, menampilkan implementasi praktis dari berbagai struktur data.

![Status](https://img.shields.io/badge/status-alpha-yellow?style=flat-square)
![Python](https://img.shields.io/badge/python-3.12-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

## 🚀 Fitur

### Fitur Utama

- ✅ **Tambah/Hapus Transaksi** - Kelola pendapatan dan pengeluaran
- ✅ **Riwayat Transaksi** - Lihat transaksi dikelompokkan berdasarkan tanggal
- ✅ **Dashboard Statistik** - Saldo, total pendapatan/pengeluaran, pengeluaran tertinggi
- ✅ **Antarmuka Mode Gelap** - Antarmuka CustomTkinter modern

### Fitur Lanjutan (BARU!)

- ✅ **Edit Transaksi** - Pembaruan di tempat menggunakan operasi DLL
- ✅ **Ekspor ke CSV** - Cadangkan transaksi dengan traversal DLL
- ✅ **Pelacak Anggaran Bulanan** - Atur anggaran dengan progress bar dan peringatan
- ✅ **Transaksi Berulang** - Jadwalkan pembayaran mingguan/bulanan
- ✅ **Pelacakan Pengeluaran Tertinggi** - Implementasi Max-Heap

## 📊 Struktur Data yang Digunakan

| Struktur Data          | Tujuan                    | Kompleksitas                                       |
| ---------------------- | ------------------------- | -------------------------------------------------- |
| **Doubly Linked List** | Simpan transaksi          | Insert/Delete: O(1), Update: O(1), Traverse: O(n)  |
| **Max-Heap**           | Lacak pengeluaran max     | Insert: O(log n), Get Max: O(1)                    |
| **Hash Map**           | Kelompok berdasarkan hari | Insert: O(1), Lookup: O(1)                         |
| **Binary Search Tree** | Riwayat anggaran          | Insert: O(log n), Search: O(log n), Traverse: O(n) |
| **Queue**              | Transaksi berulang        | Enqueue/Dequeue: O(1)                              |

## 🏗️ Struktur Proyek

```
FlowTrack/
├── models/
│   ├── finance_manager.py       # Logika bisnis inti
│   ├── transaction_node.py      # Definisi node DLL
│   ├── max_heap.py             # Implementasi Max-Heap
│   ├── recurring_queue.py       # [BARU] Queue untuk transaksi berulang
│   ├── budget_bst.py           # [BARU] BST untuk pelacakan anggaran
│   └── __init__.py
│
├── ui/
│   ├── main_window.py          # Jendela aplikasi utama
│   ├── components.py           # Komponen UI yang dapat digunakan kembali
│   └── __init__.py
│
├── utils/
│   ├── constants.py            # Konstanta UI dan warna
│   ├── helpers.py              # Fungsi pembantu
│   └── __init__.py
│
├── main.py                     # Titik masuk aplikasi
├── data.json                   # Data transaksi yang disimpan
│
├── README.md                   # File ini
├── FEATURES.md                 # Dokumentasi fitur terperinci
├── DEMO_GUIDE.md              # Panduan demo untuk profesor
└── requirements.txt           # Dependensi Python
```

## 🛠️ Instalasi

### Prasyarat

- Python 3.10+
- pip atau conda

### Pengaturan

1. **Kloning repositori**

```bash
cd d:\strukdat\FlowTrack
```

2. **Buat lingkungan virtual** (opsional tetapi direkomendasikan)

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

3. **Instal dependensi**

```bash
pip install -r requirements.txt
```

### Dependensi

- `customtkinter>=5.0` - Kerangka kerja GUI modern
- `python>=3.10` - Bahasa inti

## ▶️ Menjalankan Aplikasi

```bash
# Aktifkan lingkungan virtual
.\.venv\Scripts\activate

# Jalankan aplikasi
python main.py
```

Aplikasi akan membuka jendela GUI dengan antarmuka FlowTrack.

## 📖 Panduan Penggunaan

### Menambah Transaksi

1. Isi formulir di panel kiri:

   - **Tanggal** (Tanggal): Tanggal transaksi
   - **Judul** (Judul): Deskripsi transaksi
   - **Total** (Jumlah): Jumlah transaksi (format otomatis)
   - **Catatan** (Kategori): Kategori transaksi
   - **Type**: Pilih "Pemasukan" (Pendapatan) atau "Pengeluaran" (Pengeluaran)

2. Opsional: Tandai "🔄 Transaksi Berulang" untuk berulang bulanan/mingguan
3. Klik tombol "Tambah Transaksi"

### Mengedit Transaksi

1. Klik tombol **✎** pada kartu transaksi apa pun
2. Jendela modal terbuka dengan bidang yang dapat diedit
3. Ubah bidang sesuai kebutuhan
4. Klik "Simpan Perubahan"

### Menghapus Transaksi

1. Klik tombol **✕** pada kartu transaksi apa pun
2. Transaksi dihapus secara instan

### Menetapkan Anggaran

1. Masukkan jumlah anggaran di bagian "💰 Anggaran Bulanan"
2. Klik tombol "Atur"
3. Progress bar menunjukkan pengeluaran vs anggaran
4. Status diperbarui dengan peringatan (Hijau/Oranye/Merah)

### Mengekspor Transaksi

1. Klik tombol **"📊 Ekspor CSV"**
2. File CSV dibuat: `flowtrack_export_YYYYMMDD_HHMMSS.csv`
3. Buka di Excel atau aplikasi spreadsheet apa pun

### Membuat Transaksi Berulang

1. Saat menambah transaksi, tandai "🔄 Transaksi Berulang"
2. Pilih jenis pengulangan: "bulanan" atau "mingguan"
3. Transaksi akan dijadwalkan secara otomatis
4. Badge 🔄 muncul pada kartu transaksi

## 💡 Detail Implementasi

### Doubly Linked List (DLL)

- Transaksi disimpan dalam urutan penyisipan (terbaru terlebih dahulu)
- O(1) insert di head, O(1) delete, O(1) update
- Mendukung traversal efisien untuk ekspor

```python
# Contoh dari models/transaction_node.py
class TransactionNode:
    def __init__(self, date, title, amount, trans_type, category, trans_id):
        self.date = date
        self.next = None
        self.prev = None
```

### Max-Heap

- Melacak pengeluaran tertinggi secara efisien
- Digunakan untuk akses cepat ke pengeluaran maksimum
- Dibangun kembali ketika transaksi pengeluaran dihapus

### Binary Search Tree

- Menyimpan data anggaran per bulan
- Traversal in-order memberikan urutan kronologis
- Mendukung query jangkauan untuk filter periode

### Queue

- Menyimpan transaksi berulang yang dijadwalkan
- Prinsip FIFO untuk pemrosesan yang adil
- Perhitungan tanggal otomatis untuk kejadian berikutnya

## 📚 Dokumentasi

- **FEATURES.md** - Dokumentasi fitur terperinci dengan contoh
- **DEMO_GUIDE.md** - Panduan demo langkah demi langkah untuk profesor
- **COMPLEXITY_ANALYSIS.md** - Analisis kompleksitas waktu/ruang

## 🧪 Pengujian

Jalankan pemeriksa sintaks Python:

```bash
python -m py_compile models/*.py ui/*.py utils/*.py
```

## 🐛 Masalah Diketahui

Tidak ada pada saat ini (rilis alfa)

## 🔮 Peningkatan Masa Depan

- [ ] Kategori anggaran berganda
- [ ] Grafik/bagan riwayat anggaran
- [ ] Notifikasi email untuk peringatan anggaran
- [ ] Dukungan multi-pengguna
- [ ] Sinkronisasi cloud
- [ ] Aplikasi mobile
- [ ] Pengambilan gambar tanda terima
- [ ] Fitur pemisahan tagihan

## 📝 Catatan Kinerja

**Untuk penggunaan tipikal (< 10.000 transaksi):**

- Operasi DLL: < 1ms
- Ekspor CSV: < 100ms
- Pencarian anggaran: < 1ms
- Operasi Heap: < 1ms

**Optimisasi untuk kumpulan data besar:**

- Pertimbangkan database (SQL) untuk > 100.000 transaksi
- Pagination untuk daftar transaksi
- Lazy loading untuk riwayat

## 📄 Lisensi

Proyek ini adalah sumber terbuka dan tersedia di bawah Lisensi MIT.

## 👨‍💻 Penulis

**Tim Pengembangan FlowTrack**

- Versi: 1.0 (Alfa)
- Pembaruan Terakhir: Desember 2024
- Dibuat untuk: Demonstrasi Kursus Struktur Data

## 🤝 Berkontribusi

Kontribusi sangat diterima! Silakan kirim Pull Request.

## 📧 Kontak

Untuk pertanyaan atau saran, silakan buka masalah di GitHub.

---

**Nikmati menggunakan FlowTrack! 💰**
