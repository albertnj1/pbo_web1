from abc import ABC, abstractmethod

class Menu(ABC):
    def __init__(self, id_menu: str, nama: str, harga: float):
        self._id_menu = id_menu
        self._nama = nama
        self.__harga = float(harga)  # Private (Enkapsulasi)

    @property
    def id_menu(self):
        return self._id_menu

    @property
    def nama(self):
        return self._nama

    @property
    def harga(self):
        return self.__harga

    @abstractmethod
    def tampilkan_info(self) -> str:
        """Wajib di-override oleh subclass (Polymorphism)"""
        pass

class Makanan(Menu):
    def __init__(self, id_menu: str, nama: str, harga: float, tingkat_pedas: str = "Sedang"):
        super().__init__(id_menu, nama, harga)
        self.tingkat_pedas = tingkat_pedas

    def tampilkan_info(self) -> str:
        return f"[Makanan] {self.nama} (Pedas: {self.tingkat_pedas}) - Rp{self.harga:,.0f}"

class Minuman(Menu):
    def __init__(self, id_menu: str, nama: str, harga: float, suhu: str = "Dingin"):
        super().__init__(id_menu, nama, harga)
        self.suhu = suhu

    def tampilkan_info(self) -> str:
        return f"[Minuman] {self.nama} ({self.suhu}) - Rp{self.harga:,.0f}"
