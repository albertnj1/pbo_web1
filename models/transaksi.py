from models.pesanan import Pesanan

class Pembayaran:
    def __init__(self, id_pembayaran: str, pesanan: Pesanan, metode: str, jumlah_bayar: float):
        self.id_pembayaran = id_pembayaran
        self.pesanan = pesanan
        self.metode = metode
        self.jumlah_bayar = float(jumlah_bayar)
        self.kembalian = 0.0

    def proses_transaksi(self) -> bool:
        total = self.pesanan.hitung_total()
        if self.jumlah_bayar >= total:
            self.kembalian = self.jumlah_bayar - total
            self.pesanan.status = "Lunas"
            return True
        return False

class Laporan:
    def __init__(self):
        self.__riwayat_transaksi: list[Pembayaran] = []

    def catat_transaksi(self, pembayaran: Pembayaran):
        if pembayaran.pesanan.status == "Lunas":
            self.__riwayat_transaksi.append(pembayaran)

    def hitung_total_pendapatan(self) -> float:
        return sum(p.pesanan.hitung_total() for p in self.__riwayat_transaksi)

    def get_semua_transaksi(self) -> list[Pembayaran]:
        return self.__riwayat_transaksi
