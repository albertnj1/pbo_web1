import unittest
from datetime import date

from models import (Admin, Kasir, Laporan, Makanan, Menu, MetodePembayaran,
                    Minuman, Pembayaran, Penyimpanan, Pesanan, User)


def siapkan():
    db = Penyimpanan()
    db.isi_data_awal()
    return db, db.login("admin", "admin123"), db.login("kasir", "kasir123")


class TestMenu(unittest.TestCase):
    def test_menu_abstrak_tidak_bisa_dibuat(self):
        with self.assertRaises(TypeError):
            Menu("X", "x", 1000)

    def test_polymorphism_tampilkan_info(self):
        self.assertIn("[Makanan]", Makanan("M1", "Nasi", 5000).tampilkan_info())
        self.assertIn("[Minuman]", Minuman("D1", "Teh", 3000).tampilkan_info())

    def test_harga_tidak_valid(self):
        with self.assertRaises(ValueError):
            Makanan("M1", "Nasi", -1)
        with self.assertRaises(ValueError):
            Makanan("M1", "Nasi", 0)

    def test_harga_private_bisa_diubah_lewat_setter(self):
        m = Makanan("M1", "Nasi", 5000)
        m.harga = 6000
        self.assertEqual(m.harga, 6000)
        with self.assertRaises(ValueError):
            m.harga = -5

    def test_tingkat_pedas_dan_suhu_tervalidasi(self):
        with self.assertRaises(ValueError):
            Makanan("M1", "Nasi", 5000, "Super Pedas")
        with self.assertRaises(ValueError):
            Minuman("D1", "Teh", 3000, "Beku")


class TestPesanan(unittest.TestCase):
    def setUp(self):
        self.m = Makanan("M1", "Ayam", 18000, "Pedas")
        self.d = Minuman("D1", "Es Teh", 4000)
        self.p = Pesanan("ORD-001", "Budi")

    def test_total(self):
        self.p.tambah_item(self.m, 2)
        self.p.tambah_item(self.d, 2)
        self.assertEqual(self.p.hitung_total(), 44000)

    def test_item_sama_digabung(self):
        self.p.tambah_item(self.d, 1)
        self.p.tambah_item(self.d, 2)
        self.assertEqual(len(self.p.get_items()), 1)
        self.assertEqual(self.p.get_items()[0].jumlah, 3)

    def test_jumlah_nol_ditolak(self):
        with self.assertRaises(ValueError):
            self.p.tambah_item(self.m, 0)

    def test_get_items_adalah_salinan(self):
        self.p.tambah_item(self.m, 1)
        self.p.get_items().clear()
        self.assertEqual(len(self.p.get_items()), 1)

    def test_hapus_item(self):
        self.p.tambah_item(self.m, 1)
        self.p.hapus_item("M1")
        self.assertTrue(self.p.kosong)
        with self.assertRaises(ValueError):
            self.p.hapus_item("M1")

    def test_perubahan_harga_menu_tidak_mengubah_pesanan(self):
        self.p.tambah_item(self.m, 1)
        self.m.harga = 99000
        self.assertEqual(self.p.hitung_total(), 18000)

    def test_pesanan_lunas_tidak_bisa_diubah(self):
        self.p.tambah_item(self.m, 1)
        Pembayaran("PAY-1", self.p, "Cash", 20000).proses_transaksi()
        with self.assertRaises(ValueError):
            self.p.tambah_item(self.d, 1)


class TestPembayaran(unittest.TestCase):
    def setUp(self):
        self.p = Pesanan("ORD-001", "Budi")
        self.p.tambah_item(Makanan("M1", "Ayam", 18000, "Pedas"), 2)  # 36.000

    def test_cash_cukup_dan_kembalian(self):
        b = Pembayaran("PAY-1", self.p, "Cash", 50000)
        self.assertTrue(b.proses_transaksi())
        self.assertEqual(b.kembalian, 14000)
        self.assertEqual(self.p.status, Pesanan.STATUS_LUNAS)

    def test_cash_kurang(self):
        b = Pembayaran("PAY-1", self.p, "Cash", 10000)
        self.assertFalse(b.proses_transaksi())
        self.assertEqual(self.p.status, Pesanan.STATUS_BELUM_BAYAR)

    def test_qris_dibayar_pas(self):
        b = Pembayaran("PAY-1", self.p, "QRIS")
        self.assertTrue(b.proses_transaksi())
        self.assertEqual(b.kembalian, 0)

    def test_metode_tidak_dikenal(self):
        with self.assertRaises(ValueError):
            Pembayaran("PAY-1", self.p, "Kartu Kredit", 50000)

    def test_metode_dari_teks_tidak_peka_huruf_besar(self):
        self.assertIs(MetodePembayaran.dari_teks("  qris "), MetodePembayaran.QRIS)

    def test_tidak_bisa_bayar_dua_kali(self):
        Pembayaran("PAY-1", self.p, "Cash", 50000).proses_transaksi()
        with self.assertRaises(ValueError):
            Pembayaran("PAY-2", self.p, "Cash", 50000).proses_transaksi()

    def test_pesanan_kosong_tidak_bisa_dibayar(self):
        with self.assertRaises(ValueError):
            Pembayaran("PAY-1", Pesanan("ORD-2", "Ani"), "Cash", 1000).proses_transaksi()


class TestUser(unittest.TestCase):
    def test_user_abstrak(self):
        with self.assertRaises(TypeError):
            User("U", "x", "x", "x")

    def test_login(self):
        db, admin, kasir = siapkan()
        self.assertIsInstance(admin, Admin)
        self.assertIsInstance(kasir, Kasir)
        self.assertIsNone(db.login("admin", "salah"))
        self.assertIsNone(db.login("tidakada", "x"))

    def test_polymorphism_role(self):
        _, admin, kasir = siapkan()
        self.assertNotEqual(admin.role_info(), kasir.role_info())
        self.assertEqual((admin.role, kasir.role), ("Admin", "Kasir"))

    def test_admin_kelola_menu_dan_user(self):
        db, admin, _ = siapkan()
        admin.tambah_menu(db, Minuman("D9", "Kopi", 5000, "Panas"))
        admin.ubah_harga_menu(db, "D9", 7000)
        self.assertEqual(db.cari_menu("D9").harga, 7000)
        with self.assertRaises(ValueError):
            admin.tambah_menu(db, Minuman("D9", "Kopi 2", 5000))  # ID kembar
        admin.hapus_menu(db, "D9")
        with self.assertRaises(ValueError):
            db.cari_menu("D9")
        admin.tambah_user(db, Kasir("U03", "Kasir 2", "kasir2", "pw"))
        admin.hapus_user(db, "U03")
        with self.assertRaises(ValueError):
            admin.hapus_user(db, admin.user_id)

    def test_kasir_tidak_punya_method_admin(self):
        _, _, kasir = siapkan()
        self.assertFalse(hasattr(kasir, "tambah_menu"))


class TestLaporan(unittest.TestCase):
    def test_alur_penuh_dan_rekap(self):
        db, admin, kasir = siapkan()
        p1 = kasir.buat_pesanan(db, "A")
        p1.tambah_item(db.cari_menu("M01"), 2)
        p1.tambah_item(db.cari_menu("D01"), 2)
        kasir.proses_pembayaran(db, p1, "Cash", 50000)
        p2 = kasir.buat_pesanan(db, "B")
        p2.tambah_item(db.cari_menu("D01"), 3)
        kasir.proses_pembayaran(db, p2, "QRIS")

        r = admin.lihat_laporan(db)
        self.assertEqual(r["jumlah_transaksi"], 2)
        self.assertEqual(r["total_pendapatan"], 44000 + 12000)
        self.assertEqual(r["per_metode"]["Cash"], 44000)
        self.assertEqual(r["per_metode"]["QRIS"], 12000)
        self.assertEqual(r["menu_terlaris"][0][:2], ("Es Teh Manis", 5))
        self.assertEqual(db.laporan.jumlah_transaksi(date(2000, 1, 1)), 0)

    def test_uang_kurang_tidak_tercatat(self):
        db, _, kasir = siapkan()
        p = kasir.buat_pesanan(db, "A")
        p.tambah_item(db.cari_menu("M01"), 1)
        with self.assertRaises(ValueError):
            kasir.proses_pembayaran(db, p, "Cash", 1000)
        self.assertEqual(db.laporan.jumlah_transaksi(), 0)

    def test_transaksi_gagal_tidak_bisa_dicatat(self):
        p = Pesanan("O", "A")
        p.tambah_item(Makanan("M", "x", 1000), 1)
        with self.assertRaises(ValueError):
            Laporan().catat_transaksi(Pembayaran("P", p, "Cash", 1))


if __name__ == "__main__":
    unittest.main()
