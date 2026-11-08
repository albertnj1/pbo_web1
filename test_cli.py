"""Demo alur lengkap tanpa web: jalankan dengan `python test_cli.py`."""
from models import Makanan, Minuman, Penyimpanan

print("--- DEMO CLASS OOP KASIR ---")

db = Penyimpanan()
db.isi_data_awal()

# Polymorphism: satu perintah, hasil beda per subclass
print("\n[Menu]")
for m in db.daftar_menu():
    print(" ", m.tampilkan_info())

# Login + role
admin = db.login("admin", "admin123")
kasir = db.login("kasir", "kasir123")
print("\n[Role]")
print(" ", admin.role_info())
print(" ", kasir.role_info())

# Admin kelola menu
admin.tambah_menu(db, Minuman("D04", "Kopi Hitam", 5000, "Panas"))
admin.ubah_harga_menu(db, "D04", 6000)

# Kasir catat pesanan
order = kasir.buat_pesanan(db, "Pelanggan 1")
order.tambah_item(db.cari_menu("M01"), 2)   # 36.000
order.tambah_item(db.cari_menu("D01"), 2)   # 8.000
print(f"\n[Pesanan {order.id_pesanan}] Total: Rp{order.hitung_total():,.0f}  Status: {order.status}")

# Pembayaran
bayar = kasir.proses_pembayaran(db, order, "Cash", 50000)
print(f"Metode: {bayar.metode.value} | Dibayar: Rp{bayar.jumlah_bayar:,.0f} | Kembalian: Rp{bayar.kembalian:,.0f}")
print(f"Status sekarang: {order.status}")

# Laporan
print("\n[Laporan]")
for kunci, nilai in admin.lihat_laporan(db).items():
    print(f"  {kunci}: {nilai}")
print("\n--- SELESAI ---")
