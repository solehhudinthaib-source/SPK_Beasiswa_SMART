# SPK Penerima Beasiswa SMA — Metode SMART

Aplikasi UTS Sistem Pengambil Keputusan, dengan data studi kasus dari jurnal:

> Putra, N. P., & Sagala, J. R. (2022). Sistem Pendukung Keputusan Pemberian Beasiswa di SMAN 1
> Bangun Purba Menggunakan Metode Simple Multi Attribute Rating Technique (SMART).
> *Jurnal Informatika Kaputama (JIK)*, 6(1), 64–74.

- 6 kriteria: C1 Nilai Rata-Rata Ujian (benefit, 30), C2 Penghasilan Orang Tua (cost, 25),
  C3 Jumlah Tanggungan (benefit, 20), C4 Sikap (benefit, 10), C5 Prestasi (benefit, 10), C6 Absensi (cost, 5)
- 15 alternatif: siswa kelas X, XI, XII (data asli jurnal; sikap & prestasi dikonversi ke angka)
- Rumus SMART: w_j = R_j / ΣR_j; u_ij = (x_ij − x_min)/(x_max − x_min) untuk benefit,
  (x_max − x_ij)/(x_max − x_min) untuk cost (min/max dari data); V(a_i) = Σ w_j · u_ij
- Penerima per kelas: X Nur Ramadhani (0,833), XI Vivi Nurhaliza (0,482), XII Putri Alvanisia Saragih (0,605)

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
4. **Rentang utilitas** dapat dipilih: dari data (min-max tiap kolom, dipakai pada studi kasus ini)
   atau skala tetap dengan batas min/max yang ditentukan sendiri.
5. **Hasil perhitungan** lengkap: perangkingan, matriks awal, normalisasi bobot, nilai utilitas,
   matriks agregasi, serta **rekomendasi penerima per kelas** (1 siswa per kelas seperti jurnal).
6. **Analisis sensitivitas OAT** dengan pilihan kriteria yang diuji.
7. **Cetak / Simpan PDF** halaman hasil.
8. Identitas mahasiswa di footer (ubah `NAMA_MAHASISWA` dan `NIM_MAHASISWA` di `app.py`).
