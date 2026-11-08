from __future__ import annotations

import hashlib
import hmac
import os
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

from models.menu import Menu
from models.pesanan import Pesanan
from models.transaksi import Pembayaran

if TYPE_CHECKING:  # hanya untuk type hint, hindari import melingkar
    from models.penyimpanan import Penyimpanan


class User(ABC):
    """Kelas abstrak pengguna sistem (Abstraksi). Password disimpan sebagai hash."""

    def __init__(self, user_id: str, nama: str, username: str, password: str):
        if not str(username).strip() or not password:
            raise ValueError("Username dan password tidak boleh kosong.")
        self._user_id = user_id
        self._nama = nama
        self._username = str(username).strip()
        self.__salt = os.urandom(16)
        self.__hash = self._hash(password, self.__salt)

    @staticmethod
    def _hash(password: str, salt: bytes) -> bytes:
        return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def nama(self) -> str:
        return self._nama

    @property
    def username(self) -> str:
        return self._username

    def verifikasi_login(self, password: str) -> bool:
        return hmac.compare_digest(self._hash(password, self.__salt), self.__hash)

    @abstractmethod
    def role_info(self) -> str:
        """Polymorphic method."""

    @property
    @abstractmethod
    def role(self) -> str:
        """Nama role, dipakai untuk pengecekan hak akses di web."""


class Admin(User):
    """Admin: mengelola menu, pengguna, dan melihat laporan."""

    @property
    def role(self) -> str:
        return "Admin"

    def role_info(self) -> str:
        return "Admin: Berwenang mengelola data menu, pengguna, dan laporan."

    def tambah_menu(self, penyimpanan: Penyimpanan, menu: Menu):
        penyimpanan.tambah_menu(menu)

    def ubah_harga_menu(self, penyimpanan: Penyimpanan, id_menu: str, harga_baru: float):
        penyimpanan.cari_menu(id_menu).harga = harga_baru

    def hapus_menu(self, penyimpanan: Penyimpanan, id_menu: str):
        penyimpanan.hapus_menu(id_menu)

    def tambah_user(self, penyimpanan: Penyimpanan, user: User):
        penyimpanan.tambah_user(user)

    def hapus_user(self, penyimpanan: Penyimpanan, user_id: str):
        if user_id == self.user_id:
            raise ValueError("Admin tidak dapat menghapus akunnya sendiri.")
        penyimpanan.hapus_user(user_id)

    def lihat_laporan(self, penyimpanan: Penyimpanan, tanggal=None) -> dict:
        return penyimpanan.laporan.rekap_penjualan(tanggal)


class Kasir(User):
    """Kasir: mencatat pesanan dan memproses pembayaran."""

    @property
    def role(self) -> str:
        return "Kasir"

    def role_info(self) -> str:
        return "Kasir: Berwenang melayani pesanan dan transaksi pembayaran."

    def buat_pesanan(self, penyimpanan: Penyimpanan, nama_pelanggan: str) -> Pesanan:
        pesanan = Pesanan(penyimpanan.buat_id_pesanan(), nama_pelanggan)
        penyimpanan.simpan_pesanan(pesanan)
        return pesanan

    def proses_pembayaran(self, penyimpanan: Penyimpanan, pesanan: Pesanan,
                          metode, jumlah_bayar: Optional[float] = None) -> Pembayaran:
        """Kembalikan Pembayaran jika lunas; raise ValueError jika uang kurang."""
        pembayaran = Pembayaran(penyimpanan.buat_id_pembayaran(), pesanan, metode, jumlah_bayar)
        if not pembayaran.proses_transaksi():
            raise ValueError(
                f"Uang kurang. Total Rp{pesanan.hitung_total():,.0f}, "
                f"dibayar Rp{pembayaran.jumlah_bayar:,.0f}."
            )
        penyimpanan.laporan.catat_transaksi(pembayaran)
        return pembayaran
