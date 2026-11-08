from datetime import date, datetime
from enum import Enum
from typing import Optional

from models.pesanan import Pesanan


class MetodePembayaran(Enum):
    CASH = "Cash"
    QRIS = "QRIS"
    TRANSFER = "Transfer"

    @classmethod
    def dari_teks(cls, teks) -> "MetodePembayaran":
        """Ubah teks dari form web (mis. 'cash', 'QRIS') jadi Enum."""
        if isinstance(teks, cls):
            return teks
        for metode in cls:
            if metode.value.lower() == str(teks).strip().lower():
                return metode
        pilihan = ", ".join(m.value for m in cls)
        raise ValueError(f"Metode pembayaran '{teks}' tidak dikenal. Pilihan: {pilihan}.")


class Pembayaran:
    """Proses pembayaran satu pesanan.

    Cash: uang yang diterima harus >= total, kelebihannya jadi kembalian.
    QRIS/Transfer: dianggap dibayar pas sesuai total tagihan.
    """

    def __init__(self, id_pembayaran: str, pesanan: Pesanan, metode, jumlah_bayar: Optional[float] = None):
        self.id_pembayaran = id_pembayaran
        self.pesanan = pesanan
        self.metode = MetodePembayaran.dari_teks(metode)
        self.jumlah_bayar = float(jumlah_bayar) if jumlah_bayar not in (None, "") else 0.0
        self.kembalian = 0.0
        self.total_tagihan = 0.0  # snapshot total saat dibayar
        self.waktu: Optional[datetime] = None
        self.__berhasil = False

    @property
    def berhasil(self) -> bool:
        return self.__berhasil

    def proses_transaksi(self) -> bool:
        """True jika lunas, False jika uang cash kurang.
        Raise ValueError jika pesanan kosong / sudah dibayar."""
        if self.__berhasil or self.pesanan.status == Pesanan.STATUS_LUNAS:
            raise ValueError("Pesanan ini sudah dibayar.")
        if self.pesanan.kosong:
            raise ValueError("Pesanan kosong tidak dapat dibayar.")

        total = self.pesanan.hitung_total()
        if self.metode is not MetodePembayaran.CASH:
            self.jumlah_bayar = total
        if self.jumlah_bayar < total:
            return False

        self.total_tagihan = total
        self.kembalian = self.jumlah_bayar - total
        self.waktu = datetime.now()
        self.pesanan.tandai_lunas()
        self.__berhasil = True
        return True


class Laporan:
    """Rekap penjualan dari pembayaran yang berhasil."""

    def __init__(self):
        self.__riwayat_transaksi: list[Pembayaran] = []

    def catat_transaksi(self, pembayaran: Pembayaran):
        if not pembayaran.berhasil:
            raise ValueError("Hanya pembayaran yang berhasil yang bisa dicatat.")
        if pembayaran in self.__riwayat_transaksi:
            raise ValueError("Transaksi ini sudah tercatat.")
        self.__riwayat_transaksi.append(pembayaran)

    def get_semua_transaksi(self) -> list[Pembayaran]:
        return list(self.__riwayat_transaksi)

    def _filter(self, tanggal: Optional[date]) -> list[Pembayaran]:
        if tanggal is None:
            return self.__riwayat_transaksi
        return [p for p in self.__riwayat_transaksi if p.waktu.date() == tanggal]

    def jumlah_transaksi(self, tanggal: Optional[date] = None) -> int:
        return len(self._filter(tanggal))

    def hitung_total_pendapatan(self, tanggal: Optional[date] = None) -> float:
        return sum(p.total_tagihan for p in self._filter(tanggal))

    def rekap_per_metode(self, tanggal: Optional[date] = None) -> dict:
        hasil = {m.value: 0.0 for m in MetodePembayaran}
        for p in self._filter(tanggal):
            hasil[p.metode.value] += p.total_tagihan
        return hasil

    def menu_terlaris(self, n: int = 5, tanggal: Optional[date] = None) -> list:
        """List of (nama_menu, jumlah_terjual, pendapatan), urut dari terbanyak."""
        agregat: dict[str, list] = {}
        for p in self._filter(tanggal):
            for item in p.pesanan.get_items():
                baris = agregat.setdefault(item.menu.nama, [0, 0.0])
                baris[0] += item.jumlah
                baris[1] += item.hitung_subtotal()
        urut = sorted(agregat.items(), key=lambda kv: kv[1][0], reverse=True)
        return [(nama, jml, pendapatan) for nama, (jml, pendapatan) in urut[:n]]

    def rekap_penjualan(self, tanggal: Optional[date] = None) -> dict:
        """Ringkasan siap tampil di halaman laporan web."""
        jumlah = self.jumlah_transaksi(tanggal)
        total = self.hitung_total_pendapatan(tanggal)
        return {
            "tanggal": tanggal,
            "jumlah_transaksi": jumlah,
            "total_pendapatan": total,
            "rata_rata_transaksi": total / jumlah if jumlah else 0.0,
            "per_metode": self.rekap_per_metode(tanggal),
            "menu_terlaris": self.menu_terlaris(tanggal=tanggal),
        }
