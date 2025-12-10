# Panduan Cepat FlowTrack

Panduan cepat untuk memulai menggunakan FlowTrack.

## ⚡ Instalasi (2 menit)

### 1. Prasyarat

- Windows/Mac/Linux
- Python 3.10 atau lebih tinggi

### 2. Pengaturan

```bash
# Navigasi ke direktori proyek
cd d:\strukdat\FlowTrack

# Buat lingkungan virtual (opsional tapi direkomendasikan)
python -m venv .venv

# Aktifkan lingkungan virtual
# Windows:
.\.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Instal dependensi
pip install customtkinter
```

### 3. Jalankan Aplikasi

```bash
python main.py
```

✅ **Selesai!** Aplikasi akan membuka dalam ~2 detik.

---

## 🎮 Penggunaan Dasar (5 menit)

### Menambah Transaksi Pertama Anda

1. **Isi formulir di sisi kiri:**

   - **Tanggal** (Tanggal): Klik untuk memasukkan tanggal (default: hari ini)
   - **Judul** (Judul): "Makan Siang"
   - **Total** (Jumlah): "50000" (format otomatis ke 50.000)
   - **Catatan** (Kategori): "Makanan"
   - **Type**: Pilih "Pengeluaran" (Pengeluaran)

2. **Klik "Tambah Transaksi"**

3. **Transaksi muncul di panel kanan** dikelompokkan berdasarkan tanggal

### Menghapus Transaksi

- Klik tombol **✕** pada kartu transaksi apa pun
- Transaksi langsung dihapus

### Mengedit Transaksi

- Klik tombol **✎** pada kartu transaksi apa pun
- Modal terbuka dengan bidang yang dapat diedit
- Klik "Simpan Perubahan" untuk memperbarui

---

## 💡 Fitur Lanjutan

### 1. Pelacak Anggaran Bulanan

**Cara mengatur anggaran:**

1. Buka bagian "💰 Anggaran Bulanan"
2. Masukkan jumlah anggaran: "2000000"
3. Klik tombol "Atur"

**Fitur:**

- Progress bar menunjukkan pengeluaran vs anggaran
- 🟢 Hijau: Aman (< 80%)
- 🟠 Oranye: Peringatan (80-100%)
- 🔴 Merah: Melebihi anggaran (> 100%)

### 2. Transaksi Berulang

**Cara membuat:**

1. Saat menambah transaksi, tandai "🔄 Transaksi Berulang"
2. Pilih jenis pengulangan: "mingguan" atau "bulanan"
3. Klik "Tambah Transaksi"

**Hasil:**

- Badge 🔄 muncul pada kartu transaksi
- Transaksi dijadwalkan secara otomatis
- Kejadian berikutnya dihitung secara otomatis

### 3. Ekspor ke CSV

**Cara mengekspor:**

1. Klik tombol **"📊 Ekspor CSV"** di panel kiri
2. File dibuat: `flowtrack_export_20241210_120000.csv`
3. File disimpan di direktori akar proyek
4. Buka di Excel atau aplikasi spreadsheet apa pun

---

## 📊 Ikhtisar Dashboard

### Panel Kiri (Input & Analitik)

- **Judul Aplikasi**: FlowTrack (alfa)
- **Tombol Aksi**: Ekspor CSV
- **Formulir Input**: Tambah transaksi baru
- **Anggaran Bulanan**: Tetapkan dan lacak anggaran
- **Pengeluaran Tertinggi**: Pelacakan Max-Heap

### Panel Kanan (Riwayat Transaksi)

- **Statistik Header**: Saldo, Pendapatan, Pengeluaran
- **Feed Transaksi**: Semua transaksi dikelompokkan berdasarkan tanggal

### Statistik Diperbarui Secara Real-time

- Saldo = Pendapatan - Pengeluaran
- Total Pendapatan = Jumlah semua pendapatan
- Total Pengeluaran = Jumlah semua pengeluaran
- Pengeluaran Tertinggi = Jumlah pengeluaran maksimum

---

## 🔧 Pemecahan Masalah

### Masalah: "ModuleNotFoundError: No module named 'customtkinter'"

**Solusi:**

```bash
pip install customtkinter
```

### Masalah: Aplikasi lambat dengan banyak transaksi

**Solusi:**

- Data dimuat dari `data.json`
- Untuk 1000+ transaksi, pertimbangkan optimisasi
- Saat ini diuji hingga 10.000 transaksi

### Masalah: File CSV tidak dibuat

**Solusi:**

- Periksa apakah direktori proyek dapat ditulis
- Coba ekspor ke lokasi berbeda
- Format file: `flowtrack_export_YYYYMMDD_HHMMSS.csv`

### Masalah: Pelacakan anggaran tidak berfungsi

**Solusi:**

1. Pastikan anggaran ditetapkan untuk bulan saat ini
2. Tambahkan transaksi pengeluaran untuk melihat kemajuan
3. Segarkan tampilan (tutup dan buka kembali modal)

---

## 📚 Referensi File

```
d:\strukdat\FlowTrack\
│
├── main.py                 # Jalankan ini untuk memulai app
├── data.json              # Database transaksi
│
├── models/
│   ├── finance_manager.py    # Logika inti
│   ├── transaction_node.py   # Node DLL
│   ├── max_heap.py          # Implementasi Heap
│   ├── recurring_queue.py    # Queue untuk berulang
│   └── budget_bst.py        # BST untuk anggaran
│
├── ui/
│   ├── main_window.py       # Aplikasi utama
│   └── components.py        # Komponen UI
│
├── utils/
│   ├── constants.py         # Warna & font
│   └── helpers.py           # Fungsi pembantu
│
├── README.md                # Dokumentasi lengkap
├── FEATURES.md              # Detail fitur
├── DEMO_GUIDE.md            # Instruksi demo
└── IMPLEMENTATION_SUMMARY.md # Detail teknis
```

---

## 🎯 Tugas Umum

### Tugas: Tambah pendapatan bulanan

```
1. Isi formulir dengan detail pendapatan
2. Atur Jenis ke "Pemasukan" (Pendapatan)
3. Klik "Tambah Transaksi"
4. Lihat saldo dan pembaruan pendapatan
```

### Tugas: Lacak pengeluaran bulanan

```
1. Atur anggaran di "💰 Anggaran Bulanan"
2. Tambah transaksi pengeluaran
3. Tonton progress bar memperbarui
4. Dapatkan peringatan saat mendekati batas
```

### Tugas: Buat pembayaran berulang

```
1. Tandai "🔄 Transaksi Berulang"
2. Pilih "bulanan" atau "mingguan"
3. Tambah transaksi
4. Badge 🔄 muncul secara otomatis
```

### Tugas: Cadangkan data

```
1. Klik "📊 Ekspor CSV"
2. File disimpan secara otomatis
3. Dapat dibuka di Excel
4. Pencadangan aman dari semua transaksi
```

---

## 📱 Pintasan Keyboard

| Aksi             | Pintasan                      |
| ---------------- | ----------------------------- |
| Tambah Transaksi | Enter (setelah isi form)      |
| Tutup Modal      | ESC (dalam modal edit)        |
| Format Jumlah    | Format otomatis saat mengetik |

---

## 💰 Format Mata Uang

Jumlah diformat secara otomatis:

- Input: `50000`
- Tampilan: `Rp 50.000` atau `50,000` (berdasarkan locale)

---

## 🔐 Penyimpanan Data

### Bagaimana data disimpan:

- Simpan otomatis ke `data.json` setelah setiap transaksi
- Format JSON untuk pencadangan/transfer mudah
- Tidak terenkripsi (tambahkan di masa depan jika diperlukan)

### Cara mencadangkan:

1. Salin `data.json` ke lokasi aman
2. Atau ekspor semua ke CSV dengan tombol "Ekspor"

### Cara mengembalikan:

1. Salin `data.json` kembali ke direktori proyek
2. Restart aplikasi
3. Data akan dimuat secara otomatis

---

## 🎓 Nilai Pendidikan

### Struktur Data yang Ditunjukkan:

1. **Doubly Linked List** - Penyimpanan transaksi

   - Insert O(1), delete O(1), update O(1)
   - O(n) traversal untuk ekspor

2. **Max-Heap** - Pelacakan pengeluaran tertinggi

   - O(1) akses ke maksimum
   - O(log n) penyisipan

3. **Hash Map** - Kelompok berdasarkan tanggal

   - O(1) pencarian dan penyisipan
   - Kamus dalam Python

4. **Binary Search Tree** - Riwayat anggaran

   - Operasi O(log n)
   - Pengurutan kronologis

5. **Queue** - Transaksi berulang
   - Penjadwalan FIFO
   - Enqueue/dequeue O(1)

---

## 🚀 Tips & Praktik Terbaik

### Untuk Pelacakan Keuangan Pribadi:

1. ✅ Tambah transaksi harian untuk akurasi
2. ✅ Atur anggaran bulanan sebelumnya
3. ✅ Tinjau riwayat transaksi setiap minggu
4. ✅ Ekspor data bulanan untuk pencadangan
5. ✅ Gunakan kategori secara konsisten

### Untuk Demo ke Profesor:

1. ✅ Siapkan sampel data sebelumnya
2. ✅ Uji semua fitur sebelum demo
3. ✅ Siapkan kode di editor
4. ✅ Jelaskan kompleksitas O(n) untuk setiap operasi
5. ✅ Ajukan pertanyaan untuk melibatkan profesor

### Untuk Pengembangan:

1. ✅ Periksa kode di `models/` untuk implementasi
2. ✅ Modifikasi UI di `ui/main_window.py`
3. ✅ Tambah struktur data baru di `models/`
4. ✅ Jalankan tes: `python -m py_compile models/*.py`

---

## 📞 Dapatkan Bantuan

### Periksa Dokumentasi:

- **FEATURES.md** - Dokumentasi fitur terperinci
- **DEMO_GUIDE.md** - Demo langkah demi langkah
- **README.md** - Ringkasan proyek lengkap
- **Komentar Kode** - Penjelasan kompleksitas dan logika

### Pertanyaan Umum:

**T: Bagaimana cara menambah pendapatan berulang?**
J: Tandai "🔄 Transaksi Berulang" saat menambah, atur jenis ke "Pemasukan", pilih "bulanan" atau "mingguan".

**T: Bisakah saya mengedit transaksi lalu?**
J: Ya! Klik tombol ✎ pada kartu transaksi apa pun.

**T: Bagaimana data bertahan?**
J: Disimpan secara otomatis ke `data.json` dalam format JSON.

**T: Bisakah saya ekspor ke Excel?**
J: Ya! Klik "Ekspor CSV" dan buka file di Excel.

**T: Berapa transaksi maksimal?**
J: Diuji hingga 10.000 transaksi. Dapat diskalakan dengan database untuk dataset yang lebih besar.

---

## 🎉 Anda Siap!

Sekarang Anda dapat:

- ✅ Lacak pendapatan dan pengeluaran
- ✅ Atur dan pantau anggaran bulanan
- ✅ Buat transaksi berulang
- ✅ Ekspor data untuk pencadangan
- ✅ Pahami struktur data praktis

**Nikmati menggunakan FlowTrack! 💰**

---

**Terakhir Diperbarui**: Desember 2024  
**Versi**: 1.0 (Alfa)
