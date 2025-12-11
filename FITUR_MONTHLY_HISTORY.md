# FITUR RIWAYAT BULANAN (Monthly History)

## 📊 Deskripsi Fitur

Fitur **Riwayat Bulanan** memungkinkan user untuk melihat ringkasan total pemasukan, pengeluaran, dan balance (saldo) dari bulan-bulan sebelumnya. Setiap kali bulan berubah, statistik bulan tersebut otomatis disimpan dan dapat diakses kapan saja.

## 🎯 Fungsi Utama

### 1. **Melihat Statistik Bulan Sebelumnya**

User dapat melihat ringkasan keuangan untuk:

- November, Oktober, September, dst
- Menampilkan: Pemasukan, Pengeluaran, Balance
- Diurutkan dari bulan terbaru ke paling lama

### 2. **Tracking Tren Keuangan**

User bisa membandingkan performa keuangan antar bulan:

- Bulan ini pengeluaran berapa?
- Perbandingan dengan bulan lalu?
- Apakah trend pengeluaran naik atau turun?

### 3. **Audit & Verifikasi**

User dapat memverifikasi data historis:

- Laporan keuangan per bulan
- Dokumentasi spending patterns
- Alasan perubahan pola pengeluaran

## 🖥️ UI Layout

```
┌─────────────────────────────────┐
│ FlowTrack (alpha)               │
├─────────────────────────────────┤
│ [Export]                        │
│                                 │
│ New Transaction                 │
│ [Input form...]                 │
│                                 │
│ 💰 Anggaran Bulanan            │
│ [Atur]     [Progress bar]      │
│                                 │
│ 📊 Riwayat Bulanan             │  ← NEW!
│ ┌─────────────────────────────┐│
│ │ 📅 2024-11                  ││
│ │ ↓ Masuk: Rp 45.000.000     ││
│ │ ↑ Keluar: Rp 30.000.000    ││
│ │ ✓ Net: Rp 15.000.000       ││
│ ├─────────────────────────────┤│
│ │ 📅 2024-10                  ││
│ │ ↓ Masuk: Rp 48.000.000     ││
│ │ ↑ Keluar: Rp 32.000.000    ││
│ │ ✓ Net: Rp 16.000.000       ││
│ └─────────────────────────────┘│
└─────────────────────────────────┘
```

## 💻 Implementasi

### File: `ui/main_window.py`

**Method 1: \_create_monthly_history_section()**

```python
def _create_monthly_history_section(self, parent):
    """Menampilkan riwayat pengeluaran dan pemasukan bulan-bulan sebelumnya"""
    container = ctk.CTkFrame(parent, fg_color="transparent")
    container.pack(padx=20, pady=(0, 20), fill="x")

    # Header
    ctk.CTkLabel(container, text="📊 Riwayat Bulanan",
                 font=(UIConstants.FONT_FAMILY, 12, "bold"),
                 text_color=UIConstants.TEXT_PRIMARY).pack(side="left", anchor="w")

    # Scrollable frame untuk monthly history
    self.widgets["monthly_history_frame"] = ctk.CTkScrollableFrame(
        container,
        fg_color="transparent",
        height=150
    )
    self.widgets["monthly_history_frame"].pack(fill="both", expand=True)
```

**Method 2: \_refresh_monthly_history()**

```python
def _refresh_monthly_history(self):
    """Update monthly history display"""
    # Clear existing widgets
    for widget in self.widgets["monthly_history_frame"].winfo_children():
        widget.destroy()

    # Get monthly history dari manager
    history = self.manager.monthly_history

    if not history:
        # Tampilkan pesan jika tidak ada history
        empty_label = ctk.CTkLabel(
            self.widgets["monthly_history_frame"],
            text="Belum ada riwayat bulan sebelumnya",
            font=(UIConstants.FONT_FAMILY, 11),
            text_color=UIConstants.TEXT_SECONDARY
        )
        empty_label.pack(pady=10)
        return

    # Sort months in reverse chronological order (terbaru dulu)
    sorted_months = sorted(history.keys(), reverse=True)

    for month in sorted_months:
        data = history[month]
        income = data.get("income", 0.0)
        expense = data.get("expense", 0.0)
        balance = data.get("balance", 0.0)

        # Create month card dengan stats...
        # Menampilkan: 📅 Month, ↓ Masuk, ↑ Keluar, ✓ Net
```

### File: `models/finance_manager.py`

**Struktur Data:**

```python
self.monthly_history = {
    "2024-11": {
        "income": 45000000,
        "expense": 30000000,
        "balance": 15000000
    },
    "2024-10": {
        "income": 48000000,
        "expense": 32000000,
        "balance": 16000000
    },
    # ... bulan-bulan sebelumnya
}
```

**Method: get_monthly_history()**

```python
def get_monthly_history(self, month: str = None) -> Dict:
    """Get statistik untuk bulan tertentu dari history"""
    if month is None:
        from datetime import timedelta
        last_month_date = datetime.now() - timedelta(days=30)
        month = last_month_date.strftime("%Y-%m")

    return self.monthly_history.get(month, {
        "income": 0.0,
        "expense": 0.0,
        "balance": 0.0
    })
```

**Integration di refresh_display():**

```python
def refresh_display(self):
    # ... existing code ...

    # Update Monthly History Display
    self._refresh_monthly_history()

    # ... rest of code ...
```

## 📈 Contoh Penggunaan

### Skenario 1: Tracking Progress Bulanan

```
Desember 2024 (bulan berjalan):
- Pemasukan: Rp 50.000.000
- Pengeluaran: Rp 35.000.000
- Balance: Rp 15.000.000

Riwayat Bulanan:
📅 November 2024
- Pemasukan: Rp 45.000.000
- Pengeluaran: Rp 30.000.000
- Balance: Rp 15.000.000

📅 Oktober 2024
- Pemasukan: Rp 48.000.000
- Pengeluaran: Rp 32.000.000
- Balance: Rp 16.000.000

Analisis: Pengeluaran naik Rp 5M dari November ke Desember
```

### Skenario 2: Budget Planning

```
User lihat history:
- November: Keluar Rp 30M → Budget November Rp 40M (aman)
- Oktober: Keluar Rp 32M → Budget Oktober Rp 40M (aman)

Plan untuk Desember: Set budget Rp 35M (sesuai rata-rata)
```

### Skenario 3: Verifikasi Data

```
User ingin crosscheck pengeluaran November:
- Lihat Riwayat Bulanan → November
- Total Pengeluaran: Rp 30M
- Cocok dengan catatan manual ✓
```

## 🔄 Alur Kerja

```
User membuka aplikasi di bulan Desember
  ↓
refresh_display() dipanggil
  ↓
check_and_reset_monthly() dijalankan
  ↓
Bulan sudah berubah dari November?
  ├─ Ya → Save November stats ke monthly_history
  │     → Reset income/expense ke 0
  │     → Update current_month ke Desember
  └─ Tidak → Lanjut normal
  ↓
_refresh_monthly_history() dipanggil
  ↓
Ambil data dari manager.monthly_history
  ↓
Render monthly cards (Desember-1, Desember-2, dll)
  ↓
Display di UI dengan format:
📅 Bulan
↓ Pemasukan: Rp X
↑ Pengeluaran: Rp Y
✓ Balance: Rp Z
```

## 📊 Data Persistence

Monthly history disimpan di `data.json`:

```json
{
  "transactions": [...],
  "current_month": "2024-12",
  "total_income": 50000000,
  "total_expense": 35000000,
  "monthly_history": {
    "2024-11": {
      "income": 45000000,
      "expense": 30000000,
      "balance": 15000000
    },
    "2024-10": {
      "income": 48000000,
      "expense": 32000000,
      "balance": 16000000
    }
  }
}
```

## ⚡ Performa

- **Time Complexity**: O(1) untuk akses bulan tertentu, O(m) untuk display semua (m = jumlah bulan)
- **Space Complexity**: O(m) dimana m = jumlah bulan dalam history
- **Update Frequency**: Setiap kali refresh_display() dipanggil
- **Impact**: Minimal (sorting & rendering saja)

## ✨ Fitur Tambahan (Future)

1. **Filter by Date Range**: Tampilkan history untuk range tertentu
2. **Export Monthly Report**: Download laporan bulanan sebagai PDF/Excel
3. **Monthly Comparison**: Bandingkan 2 bulan berbeda side-by-side
4. **Trend Chart**: Visualisasi grafik spending trend
5. **Monthly Forecast**: Prediksi spending berdasarkan trend
6. **Monthly Goals**: Set target pengeluaran per bulan

## 🎯 Manfaat

✅ Mudah melihat history keuangan per bulan
✅ Tracking tren spending jangka panjang
✅ Data verification & audit trail
✅ Planning & budgeting lebih baik
✅ Automatic (tanpa action user)
✅ Data tersimpan permanent di history
✅ Tidak bercampur dengan bulan berjalan
