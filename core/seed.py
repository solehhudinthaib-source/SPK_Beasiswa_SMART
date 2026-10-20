"""Data studi kasus awal.

Sumber: Nicko Permana Putra & Jijon Raphita Sagala (2022). Sistem Pendukung Keputusan
Pemberian Beasiswa di SMAN 1 Bangun Purba Menggunakan Metode SMART.
Jurnal Informatika Kaputama (JIK), Vol. 6 No. 1, hlm. 64-74.

Nilai performa = Tabel 10 jurnal (data Tabel 9 yang sudah dikonversi ke nilai
sub-kriteria 20-100). Semua kriteria bertipe benefit karena konversi sub-kriteria
sudah membuat nilai lebih tinggi = lebih layak menerima beasiswa (mis. penghasilan
orang tua <= 1 juta diberi nilai 100).
"""

JOURNAL_PROJECT_NAME = "Beasiswa SMAN 1 Bangun Purba"

JOURNAL_DATA = {
    "criteria": [
        "C1 Nilai Rata-Rata Ujian",
        "C2 Penghasilan Orang Tua",
        "C3 Jumlah Tanggungan",
        "C4 Sikap",
        "C5 Prestasi",
        "C6 Absensi",
    ],
    "types": ["benefit"] * 6,
    "weights": [30.0, 25.0, 20.0, 10.0, 10.0, 5.0],
    "weight_method": "direct",
    "utility_mode": "scale",
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
        [60, 80, 60, 80, 20, 80],
        [60, 60, 40, 80, 40, 100],
        [60, 80, 20, 80, 20, 80],
        [80, 60, 60, 100, 60, 100],
        [60, 40, 80, 80, 20, 80],
        [40, 60, 40, 80, 40, 80],
        [40, 60, 60, 80, 20, 80],
        [40, 80, 20, 60, 20, 60],
        [20, 60, 40, 100, 40, 100],
        [40, 40, 40, 100, 60, 80],
        [20, 80, 20, 100, 40, 100],
        [40, 60, 40, 100, 40, 80],
        [40, 40, 80, 100, 60, 80],
        [40, 60, 60, 60, 20, 60],
        [40, 40, 60, 80, 20, 80],
    ],
}


def seed_default_project():
    from core.models import Project
    return Project(
        name=JOURNAL_PROJECT_NAME,
        description=("Rekomendasi penerima beasiswa SMA: 6 kriteria, 15 siswa kelas X-XII. "
                     "Data: Jurnal Informatika Kaputama Vol. 6 No. 1 (2022)."),
        data_json=JOURNAL_DATA,
    )
