from flask import Flask, render_template, request, redirect, url_for, flash

# 1. Mengambil (Import) class buatan Albert di folder models
from models.menu import Makanan, Minuman
from models.transaksi import Pesanan, Pembayaran
from models.user import Kasir

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_gilang'

# Data Dummy Kasir & Menu
kasir_aktif = Kasir("K01", "Gilang", "gilang", "123")

daftar_menu = {
    1: Makanan(id_menu=1, nama="Nasi Goreng", harga=15000, stok=10),
    2: Minuman(id_menu=2, nama="Es Teh Manis", harga=5000, stok=20)
}

pesanan_aktif = Pesanan(id_pesanan="TRX-001", kasir=kasir_aktif)

# Route Halaman Utama Kasir
@app.route('/', methods=['GET'])
def index():
    return render_template('kasir.html', kasir=kasir_aktif, menu_list=daftar_menu.values(), pesanan=pesanan_aktif)

# Route Tambah Item (Tangkap Form & Panggil Method Albert)
@app.route('/tambah-item', methods=['POST'])
def tambah_item():
    id_menu = int(request.form.get('id_menu'))
    jumlah = int(request.form.get('jumlah'))
    
    menu_terpilih = daftar_menu.get(id_menu)
    if menu_terpilih:
        # PANGGIL METHOD OOP ALBERT
        pesanan_aktif.tambah_item(menu_terpilih, jumlah)
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)