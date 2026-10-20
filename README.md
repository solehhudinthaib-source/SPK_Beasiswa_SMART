# SPK Penerima Beasiswa SMA — Metode SMART

Aplikasi UTS Sistem Pengambil Keputusan, dengan data studi kasus dari jurnal:

> Putra, N. P., & Sagala, J. R. (2022). Sistem Pendukung Keputusan Pemberian Beasiswa di SMAN 1
> Bangun Purba Menggunakan Metode Simple Multi Attribute Rating Technique (SMART).
> *Jurnal Informatika Kaputama (JIK)*, 6(1), 64–74.

- 6 kriteria: C1 Nilai Rata-Rata Ujian (30), C2 Penghasilan Orang Tua (25), C3 Jumlah Tanggungan (20),
  C4 Sikap (10), C5 Prestasi (10), C6 Absensi (5)
- 15 alternatif: siswa kelas X, XI, XII
- Hasil aplikasi sama persis dengan Tabel 11 jurnal (Nur Ramadhani 0,65 peringkat 1)

## Cara menjalankan

```
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

Buka http://127.0.0.1:5000/. Saat pertama dijalankan, database otomatis berisi studi kasus
"Beasiswa SMAN 1 Bangun Purba".

## Fitur

1. **Manajemen studi kasus** — buat, buka, dan hapus beberapa kasus keputusan.
2. **Input matriks** kriteria (benefit/cost, bobot) dan alternatif, termasuk kolom **Kelas**;
   impor dari CSV/Excel dan ekspor ke Excel.
3. **Metode pembobotan**: Direct Rating, Swing, Rank Order Centroid (ROC), atau bobot merata.
4. **Rentang utilitas** dapat dipilih: dari data (min-max tiap kolom) atau **skala tetap
   sub-kriteria** (min 20, max 100) sesuai jurnal: u = (C_out − C_min) / (C_max − C_min).
5. **Hasil perhitungan** lengkap: perangkingan, matriks awal, normalisasi bobot, nilai utilitas,
   matriks agregasi, serta **rekomendasi penerima per kelas** (1 siswa per kelas seperti jurnal).
6. **Analisis sensitivitas OAT** dengan pilihan kriteria yang diuji.
7. **Cetak / Simpan PDF** halaman hasil.
8. Identitas mahasiswa di footer (ubah `NAMA_MAHASISWA` dan `NIM_MAHASISWA` di `app.py`).
