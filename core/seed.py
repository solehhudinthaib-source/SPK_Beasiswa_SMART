"""Data studi kasus awal.

Sumber data: Nicko Permana Putra & Jijon Raphita Sagala (2022). Sistem Pendukung Keputusan
Pemberian Beasiswa di SMAN 1 Bangun Purba Menggunakan Metode SMART.
Jurnal Informatika Kaputama (JIK), Vol. 6 No. 1, hlm. 64-74.

Nilai performa = data asli Tabel 9 jurnal. Penghasilan orang tua (juta Rp) dan absensi (hari)
bertipe cost. Sikap dan prestasi (kualitatif) dikonversi ke angka memakai skala sub-kriteria
jurnal (Sangat Baik = 100 ... Tidak Baik = 20; Juara Provinsi/Nasional = 100 ... Tidak Ada = 20).
Utilitas memakai nilai minimum dan maksimum dari data (rumus SMART materi Bab 7).
"""

JOURNAL_PROJECT_NAME = "Beasiswa SMAN 1 Bangun Purba"

JOURNAL_DATA = {
    "criteria": [
        "C1 Nilai Rata-Rata Ujian",
        "C2 Penghasilan Ortu (juta)",
        "C3 Jumlah Tanggungan",
        "C4 Sikap",
        "C5 Prestasi",
        "C6 Absensi (hari)",
    ],
    "types": ["benefit", "cost", "benefit", "benefit", "benefit", "cost"],
    "weights": [30.0, 25.0, 20.0, 10.0, 10.0, 5.0],
    "weight_method": "direct",
    "utility_mode": "data",
    "scale_min": 20.0,
    "scale_max": 100.0,
    "alternatives": [
        "Alika Wulandari Lubis",
        "M. Rafli Saldani Barus",
        "Nazwa Afrida Putri",
        "Nur Ramadhani",
        "Maharani Purba",
        "Tina Anasti Putri Pinem",
        "Yuni Rohimah Saragih",
        "Rismawati Saragih",
        "Lira Virna",
        "Vivi Nurhaliza",
        "Muhammad Aldi",
        "Margaret Purba",
        "Putri Alvanisia Saragih",
        "Anggi Novita Ramadhani",
        "Cristin Natalia Siahaan",
    ],
    "groups": ["X"] * 5 + ["XI"] * 5 + ["XII"] * 5,
    "performance": [
        [86, 2.0, 3, 80, 20, 2],
        [87, 3.0, 2, 80, 40, 0],
        [87, 1.8, 1, 80, 20, 1],
        [90, 2.5, 3, 100, 60, 0],
        [87, 4.0, 4, 80, 20, 1],
        [80, 2.5, 2, 80, 40, 2],
        [80, 3.0, 3, 80, 20, 1],
        [81, 1.5, 1, 60, 20, 4],
        [75, 2.5, 2, 100, 40, 0],
        [82, 3.5, 2, 100, 60, 2],
        [79, 2.0, 1, 100, 40, 0],
        [83, 2.8, 2, 100, 40, 1],
        [84, 4.0, 4, 100, 60, 2],
        [80, 3.0, 3, 60, 20, 3],
        [81, 3.5, 3, 80, 20, 1],
    ],
}


def seed_default_project():
    from core.models import Project
    return Project(
        name=JOURNAL_PROJECT_NAME,
        description=("Rekomendasi penerima beasiswa SMA: 6 kriteria (4 benefit, 2 cost), 15 siswa kelas X-XII. "
                     "Data: Jurnal Informatika Kaputama Vol. 6 No. 1 (2022)."),
        data_json=JOURNAL_DATA,
    )
