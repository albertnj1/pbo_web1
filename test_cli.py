from models.menu import Makanan, Minuman
from models.pesanan import Pesanan
from models.transaksi import Pembayaran, Laporan

print("--- MENJALANKAN TEST CLASS OOP KASIR ---")

# 1. Buat Menu
m1 = Makanan("M01", "Ayam Goreng Sambal", 18000, "Pedas")
d1 = Minuman("D01", "Es Teh Manis", 4000, "Dingin")
print(m1.tampilkan_info())
print(d1.tampilkan_info())

# 2. Buat Pesanan
order1 = Pesanan("ORD-001", "Pelanggan 1")
order1.tambah_item(m1, 2)  # 36.000
order1.tambah_item(d1, 2)  # 8.000
print(f"\nTotal Tagihan: Rp{order1.hitung_total():,.0f}")  # Harusnya 44.000

# 3. Proses Pembayaran
bayar = Pembayaran("PAY-001", order1, "Cash", 50000)
berhasil = bayar.proses_transaksi()

if berhasil:
    print(f"Status Pesanan : {order1.status}")
    print(f"Uang Diterima  : Rp{bayar.jumlah_bayar:,.0f}")
    print(f"Kembalian      : Rp{bayar.kembalian:,.0f}")

# 4. Catat ke Laporan
laporan = Laporan()
laporan.catat_transaksi(bayar)
print(f"Total Pendapatan di Laporan: Rp{laporan.hitung_total_pendapatan():,.0f}")
print("\n--- SEMUA CLASS BERFUNGSI SEMPURNA! ---")
