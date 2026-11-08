from abc import ABC, abstractmethod


class Menu(ABC):
    """Kelas abstrak untuk semua item menu (Abstraksi).

    Tidak bisa dibuat objeknya langsung; harus lewat Makanan atau Minuman.
    """

    def __init__(self, id_menu: str, nama: str, harga: float):
        if not str(id_menu).strip():
            raise ValueError("ID menu tidak boleh kosong.")
        if not str(nama).strip():
            raise ValueError("Nama menu tidak boleh kosong.")
        self._id_menu = str(id_menu).strip()
        self._nama = str(nama).strip()
        self.__harga = self._validasi_harga(harga)  # Private (Enkapsulasi)

    @staticmethod
    def _validasi_harga(harga) -> float:
        harga = float(harga)
        if harga <= 0:
            raise ValueError("Harga harus lebih dari 0.")
        return harga

    @property
    def id_menu(self) -> str:
        return self._id_menu

    @property
    def nama(self) -> str:
        return self._nama

    @property
    def harga(self) -> float:
        return self.__harga

    @harga.setter
    def harga(self, harga_baru: float):
        self.__harga = self._validasi_harga(harga_baru)

    @property
    @abstractmethod
    def kategori(self) -> str:
        """Nama kategori menu. Wajib di-override subclass."""

    @abstractmethod
    def tampilkan_info(self) -> str:
        """Wajib di-override oleh subclass (Polymorphism)."""


class Makanan(Menu):
    TINGKAT_PEDAS = ("Tidak Pedas", "Sedang", "Pedas")

    def __init__(self, id_menu: str, nama: str, harga: float, tingkat_pedas: str = "Sedang"):
        super().__init__(id_menu, nama, harga)
        self.tingkat_pedas = tingkat_pedas

    @property
    def tingkat_pedas(self) -> str:
        return self._tingkat_pedas

    @tingkat_pedas.setter
    def tingkat_pedas(self, nilai: str):
        if nilai not in self.TINGKAT_PEDAS:
            raise ValueError(f"Tingkat pedas harus salah satu dari {self.TINGKAT_PEDAS}.")
        self._tingkat_pedas = nilai

    @property
    def kategori(self) -> str:
        return "Makanan"

    def tampilkan_info(self) -> str:
        return f"[Makanan] {self.nama} (Pedas: {self.tingkat_pedas}) - Rp{self.harga:,.0f}"


class Minuman(Menu):
    SUHU = ("Dingin", "Hangat", "Panas")

    def __init__(self, id_menu: str, nama: str, harga: float, suhu: str = "Dingin"):
        super().__init__(id_menu, nama, harga)
        self.suhu = suhu

    @property
    def suhu(self) -> str:
        return self._suhu

    @suhu.setter
    def suhu(self, nilai: str):
        if nilai not in self.SUHU:
            raise ValueError(f"Suhu harus salah satu dari {self.SUHU}.")
        self._suhu = nilai

    @property
    def kategori(self) -> str:
        return "Minuman"

    def tampilkan_info(self) -> str:
        return f"[Minuman] {self.nama} ({self.suhu}) - Rp{self.harga:,.0f}"
