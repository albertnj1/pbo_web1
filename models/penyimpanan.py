from __future__ import annotations

from typing import Optional

from models.menu import Makanan, Menu, Minuman
from models.pesanan import Pesanan
from models.transaksi import Laporan
from models.user import Admin, Kasir, User


class Penyimpanan:
    """Tempat data aplikasi disimpan di memori selama server Flask hidup.

    Data hilang saat server restart. Cukup untuk tugas PBO; kalau mau permanen,
    cukup ganti isi class ini (mis. ke JSON/SQLite) tanpa mengubah class lain.
    """

    def __init__(self):
        self.__menu: dict[str, Menu] = {}
        self.__users: dict[str, User] = {}
        self.__pesanan: dict[str, Pesanan] = {}
        self.__laporan = Laporan()
        self.__no_pesanan = 0
        self.__no_pembayaran = 0

    @property
    def laporan(self) -> Laporan:
        return self.__laporan

    # --- Menu ---
    def tambah_menu(self, menu: Menu):
        if menu.id_menu in self.__menu:
            raise ValueError(f"ID menu '{menu.id_menu}' sudah dipakai.")
        self.__menu[menu.id_menu] = menu

    def cari_menu(self, id_menu: str) -> Menu:
        if id_menu not in self.__menu:
            raise ValueError(f"Menu '{id_menu}' tidak ditemukan.")
        return self.__menu[id_menu]

    def hapus_menu(self, id_menu: str):
        self.cari_menu(id_menu)
        del self.__menu[id_menu]

    def daftar_menu(self, kategori: Optional[str] = None) -> list[Menu]:
        semua = list(self.__menu.values())
        if kategori is None:
            return semua
        return [m for m in semua if m.kategori == kategori]

    # --- User ---
    def tambah_user(self, user: User):
        if any(u.username == user.username for u in self.__users.values()):
            raise ValueError(f"Username '{user.username}' sudah dipakai.")
        if user.user_id in self.__users:
            raise ValueError(f"ID user '{user.user_id}' sudah dipakai.")
        self.__users[user.user_id] = user

    def hapus_user(self, user_id: str):
        if user_id not in self.__users:
            raise ValueError(f"User '{user_id}' tidak ditemukan.")
        del self.__users[user_id]

    def daftar_user(self) -> list[User]:
        return list(self.__users.values())

    def login(self, username: str, password: str) -> Optional[User]:
        """Kembalikan User jika username+password cocok, selain itu None."""
        for user in self.__users.values():
            if user.username == username and user.verifikasi_login(password):
                return user
        return None

    # --- Pesanan ---
    def buat_id_pesanan(self) -> str:
        self.__no_pesanan += 1
        return f"ORD-{self.__no_pesanan:03d}"

    def buat_id_pembayaran(self) -> str:
        self.__no_pembayaran += 1
        return f"PAY-{self.__no_pembayaran:03d}"

    def simpan_pesanan(self, pesanan: Pesanan):
        self.__pesanan[pesanan.id_pesanan] = pesanan

    def cari_pesanan(self, id_pesanan: str) -> Pesanan:
        if id_pesanan not in self.__pesanan:
            raise ValueError(f"Pesanan '{id_pesanan}' tidak ditemukan.")
        return self.__pesanan[id_pesanan]

    def daftar_pesanan(self, status: Optional[str] = None) -> list[Pesanan]:
        semua = list(self.__pesanan.values())
        if status is None:
            return semua
        return [p for p in semua if p.status == status]

    # --- Data awal untuk demo ---
    def isi_data_awal(self):
        self.tambah_user(Admin("U01", "Admin Warung", "admin", "admin123"))
        self.tambah_user(Kasir("U02", "Kasir 1", "kasir", "kasir123"))
        self.tambah_menu(Makanan("M01", "Ayam Goreng Sambal", 18000, "Pedas"))
        self.tambah_menu(Makanan("M02", "Nasi Putih", 5000, "Tidak Pedas"))
        self.tambah_menu(Makanan("M03", "Soto Ayam", 15000, "Sedang"))
        self.tambah_menu(Minuman("D01", "Es Teh Manis", 4000, "Dingin"))
        self.tambah_menu(Minuman("D02", "Teh Hangat", 3000, "Hangat"))
        self.tambah_menu(Minuman("D03", "Es Jeruk", 6000, "Dingin"))
