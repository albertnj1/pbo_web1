from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, user_id: str, nama: str):
        self._user_id = user_id
        self._nama = nama

    @property
    def nama(self):
        return self._nama

    @abstractmethod
    def role_info(self) -> str:
        """Polymorphic method"""
        pass

class Admin(User):
    def role_info(self) -> str:
        return "Admin: Berwenang mengelola data menu dan laporan."

class Kasir(User):
    def role_info(self) -> str:
        return "Kasir: Berwenang melayani pesanan dan transaksi pembayaran."
