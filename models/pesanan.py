from datetime import datetime
from models.menu import Menu

class DetailPesanan:
    """Relasi Agregasi ke Menu"""
    def __init__(self, menu: Menu, jumlah: int):
        self.__menu = menu
        self.__jumlah = int(jumlah)

    @property
    def menu(self):
        return self.__menu

    @property
    def jumlah(self):
        return self.__jumlah

    def hitung_subtotal(self) -> float:
        return self.__menu.harga * self.__jumlah

class Pesanan:
    """Relasi Komposisi ke DetailPesanan"""
    def __init__(self, id_pesanan: str, nama_pelanggan: str):
        self.id_pesanan = id_pesanan
        self.nama_pelanggan = nama_pelanggan
        self.waktu = datetime.now()
        self.__items: list[DetailPesanan] = []
        self.status = "Belum Bayar"

    def tambah_item(self, menu: Menu, jumlah: int):
        if jumlah > 0:
            detail = DetailPesanan(menu, jumlah)
            self.__items.append(detail)

    def hitung_total(self) -> float:
        return sum(item.hitung_subtotal() for item in self.__items)

    def get_items(self) -> list[DetailPesanan]:
        return self.__items
