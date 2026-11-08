from datetime import datetime

from models.menu import Menu


class DetailPesanan:
    """Satu baris item dalam pesanan. Relasi Agregasi ke Menu.

    Harga satuan disalin (snapshot) saat item dibuat, supaya perubahan harga
    menu di kemudian hari tidak mengubah total pesanan yang sudah ada.
    """

    def __init__(self, menu: Menu, jumlah: int):
        jumlah = int(jumlah)
        if jumlah <= 0:
            raise ValueError("Jumlah item harus lebih dari 0.")
        self.__menu = menu
        self.__jumlah = jumlah
        self.__harga_satuan = menu.harga

    @property
    def menu(self) -> Menu:
        return self.__menu

    @property
    def jumlah(self) -> int:
        return self.__jumlah

    @property
    def harga_satuan(self) -> float:
        return self.__harga_satuan

    def tambah_jumlah(self, tambahan: int):
        tambahan = int(tambahan)
        if tambahan <= 0:
            raise ValueError("Jumlah tambahan harus lebih dari 0.")
        self.__jumlah += tambahan

    def hitung_subtotal(self) -> float:
        return self.__harga_satuan * self.__jumlah


class Pesanan:
    """Pesanan pelanggan. Relasi Komposisi ke DetailPesanan:
    DetailPesanan dibuat dan dimiliki oleh Pesanan, tidak berdiri sendiri."""

    STATUS_BELUM_BAYAR = "Belum Bayar"
    STATUS_LUNAS = "Lunas"

    def __init__(self, id_pesanan: str, nama_pelanggan: str):
        if not str(nama_pelanggan).strip():
            raise ValueError("Nama pelanggan tidak boleh kosong.")
        self.id_pesanan = id_pesanan
        self.nama_pelanggan = str(nama_pelanggan).strip()
        self.waktu = datetime.now()
        self.__items: list[DetailPesanan] = []
        self.__status = self.STATUS_BELUM_BAYAR

    @property
    def status(self) -> str:
        return self.__status

    @property
    def kosong(self) -> bool:
        return len(self.__items) == 0

    def _pastikan_belum_lunas(self):
        if self.__status == self.STATUS_LUNAS:
            raise ValueError("Pesanan sudah lunas dan tidak dapat diubah.")

    def tambah_item(self, menu: Menu, jumlah: int):
        self._pastikan_belum_lunas()
        for item in self.__items:
            if item.menu.id_menu == menu.id_menu:
                item.tambah_jumlah(jumlah)
                return
        self.__items.append(DetailPesanan(menu, jumlah))

    def hapus_item(self, id_menu: str):
        self._pastikan_belum_lunas()
        sebelum = len(self.__items)
        self.__items = [i for i in self.__items if i.menu.id_menu != id_menu]
        if len(self.__items) == sebelum:
            raise ValueError(f"Menu '{id_menu}' tidak ada di pesanan ini.")

    def hitung_total(self) -> float:
        return sum(item.hitung_subtotal() for item in self.__items)

    def get_items(self) -> list[DetailPesanan]:
        return list(self.__items)  # salinan, supaya list asli tetap terlindungi

    def tandai_lunas(self):
        """Dipanggil oleh Pembayaran setelah pembayaran berhasil."""
        self.__status = self.STATUS_LUNAS
