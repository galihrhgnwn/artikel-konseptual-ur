# Daftar ketentuan template (satu per satu)

Sumber: PDF "Template Artikel Konseptual E1" — Universitas Riau, Bahasa Indonesia 2026/2027.
Kolom **Ditegakkan oleh**: `build` = otomatis oleh build_docx.py; `check` = diperiksa check_article.py; `manual` = penulis/agen wajib memeriksa sendiri.

## A. Halaman dan format dokumen

| No | Ketentuan | Ditegakkan oleh |
|---|---|---|
| A1 | Kertas A4; margin kiri/kanan/atas 2,2 cm, bawah 2,0 cm (diukur dari PDF template) | build |
| A2 | Font Lato di seluruh dokumen; isi Pendahuluan–Simpulan Lato 11, spasi 1, rata kiri-kanan, alinea menjorok 1 cm | build |
| A3 | Header: teks merah tebal rata kanan "Artikel Konseptual – Mata Kuliah Bahasa Indonesia Kelas E1 Tempuk Manggis 9" + kotak nomor halaman abu-abu (7F7F7F, angka putih), garis abu-abu (D9D9D9) di bawahnya. Nomor halaman memakai field PAGE sungguhan (di PDF template semua halaman tercetak "2" karena artefak ekspor). Teks header diubah lewat `header` di article.json bila kelas pengguna berbeda | build |
| A4 | Footer: bilah abu gelap (404040), teks putih Arial 9 rata tengah "Universitas Riau – Bahasa Indonesia 2026/2027", garis biru (4F81BD) di atas bilah | build |
| A5 | Bahasa dokumen diset id-ID (pemeriksa ejaan Indonesia) | build |
| A6 | Lato bawaan skill di `assets/fonts` (Regular, Italic, Bold, BoldItalic; OFL) dipasang oleh `install_fonts.sh` agar pratinjau akurat; nama font di berkas tetap Lato. Ingatkan pengguna memasang Lato di komputernya | build |

## B. Judul, penulis, abstrak

| No | Ketentuan | Ditegakkan oleh |
|---|---|---|
| B1 | Judul lugas dan menarik, sesuai bidang/program studi, maksimal 12 kata | check + manual |
| B2 | Judul Lato 24 tebal, rata tengah | build |
| B3 | Baris penulis: "Nama Penulis" tebal + superskrip 1 + simbol amplop (✉) penanda corresponding author | build |
| B4 | Baris afiliasi: "(1) Nama Program Studi, Nama Perguruan Tinggi" | build + check |
| B5 | Di kiri bawah: "✉ Corresponding author" lalu "(email corresponding author)" — Arial 9 | build |
| B6 | Judul bagian "Abstrak" (huruf awal kapital, bukan semua kapital), tebal, rata tengah; kemudian "Abstract" dengan gaya sama | build |
| B7 | Abstrak ditulis dalam Bahasa Indonesia DAN Bahasa Inggris | check |
| B8 | Satu alinea, 100–150 kata, Lato 11 spasi 1 (maksimal 150) | check |
| B9 | Berdiri sendiri: tanpa kutipan/sitasi, tanpa gambar/tabel, tanpa format persamaan | check |
| B10 | Isi abstrak berurutan: latar masalah singkat (1–2 kalimat) → tujuan jelas → pendekatan singkat (telaah literatur) → ringkasan argumen/temuan utama → kesimpulan singkat | manual |
| B11 | Berfungsi "iklan artikel": menyebut apa yang dibahas dan menonjolkan argumen utama; akurat, singkat, jelas, spesifik; kata mencerminkan arti sebenarnya; jujur ("precise and honest") | manual |
| B12 | Hindari jargon teknis dan singkatan tidak umum | manual |
| B13 | Abstract (Inggris) huruf miring seluruhnya; terjemahan setara abstrak Indonesia | build + manual |
| B14 | "Kata Kunci:" label tebal, isi miring, indentasi menggantung; "Keyword:" untuk Inggris; maksimal 5 konsep, dipisah titik koma (;), mewakili bidang program studi | build + check |

## C. Pendahuluan

| No | Ketentuan | Ditegakkan oleh |
|---|---|---|
| C1 | Judul bagian PENDAHULUAN (kapital, tebal, rata kiri); 250–350 kata | build + check |
| C2 | Urutan: latar belakang yang memadai (maksimal 1 paragraf) → tinjauan literatur sangat singkat → tujuan penulisan di AKHIR bagian | manual + check (kata "tujuan") |
| C3 | Tinjauan literatur menyebut solusi/metode yang ada, mana yang terbaik, batasan utama penelitian sebelumnya, apa yang ingin dicapai (mengatasi keterbatasan), dan manfaat ilmiah/kebaruan artikel | manual |
| C4 | Hindari survei literatur terperinci dan ringkasan hasil | manual |
| C5 | JANGAN menulis tinjauan sebagai "penulis A menyatakan…, penulis B menyatakan…"; sajikan sebagai kelompok per metode/topik yang merujuk beberapa literatur sekaligus, mis. "(A, 2020; B, 2021; C, 2022)" | manual |

## D. Ketentuan artikel konseptual

| No | Ketentuan | Ditegakkan oleh |
|---|---|---|
| D1 | Judul, topik, dan isi sesuai bidang/program studi penulis | manual |
| D2 | Disusun dari telaah literatur ilmiah; SATU argumen utama yang dibela sepanjang tulisan; tanpa pengumpulan data lapangan (tidak ada survei, wawancara, eksperimen milik penulis) | manual |
| D3 | Isi Pendahuluan sampai Simpulan minimal 1.000 kata; tidak dihitung: judul, nama penulis, abstrak, kata kunci, tabel dan gambar beserta keterangannya, ucapan terima kasih, daftar pustaka | check |
| D4 | Target: Pendahuluan 250–350, Pembahasan 700–900, Simpulan 80–100 kata | check |
| D5 | Hapus seluruh teks petunjuk template sebelum dikumpulkan | check |

## E. Kaidah bahasa dan etika

| No | Ketentuan | Ditegakkan oleh |
|---|---|---|
| E1 | Bahasa Indonesia baku, ejaan benar (PUEBI/EYD sesuai KBBI) | manual + check (kata tidak baku) |
| E2 | Istilah asing ditulis miring (`*istilah*`) | check (peringatan) + manual |
| E3 | Kalimat efektif dan objektif; hindari kata "saya", opini tanpa dukungan, kata mubazir | check |
| E4 | Satu paragraf memuat satu gagasan pokok | check (peringatan >9 kalimat) + manual |
| E5 | Karya sendiri; menyalin tanpa rujukan adalah plagiarisme → parafrase total | manual |
| E6 | Memakai alat bantu penulisan → penulis tetap bertanggung jawab memeriksa isi dan SELURUH rujukan (ingatkan pengguna membuka DOI/tautan sendiri) | manual (pesan penutup) |

## F. Pembahasan

| No | Ketentuan | Ditegakkan oleh |
|---|---|---|
| F1 | Bagian terpenting; menggantikan Metode Penelitian serta Hasil dan Pembahasan; 700–900 kata | check |
| F2 | 3–5 subjudul dicetak tebal; tiap subjudul membangun satu bagian argumen dan didukung rujukan | build + check |
| F3 | Mulai dengan ringkasan singkat argumen utama (bukan ringkasan seluruh literatur) → bidang `pengantar` | manual |
| F4 | Seluruh isi berkaitan dengan bidang/program studi penulis | manual |
| F5 | Wajib mencakup (a) bagaimana pembahasan menjawab tujuan di akhir Pendahuluan dan apa argumen utama (apa/bagaimana); (b) penjelasan/interpretasi ilmiah tiap gagasan yang didukung literatur valid (mengapa); (c) apakah pandangan antarsumber sejalan — bila berbeda, jelaskan letak perbedaan dan sikap penulis (apa lagi) | manual |
| F6 | Contoh susunan subjudul: Konsep dan Perkembangan [Topik]; Analisis [Masalah] pada Bidang [Program Studi]; Keterkaitan [Konsep A] dan [Konsep B]; Implikasi bagi [Bidang Program Studi]; Keterbatasan Kajian | manual |
| F7 | Hindari daftar kutipan berurutan; bandingkan dan tafsirkan sumber dengan kalimat sendiri | manual |

## G. Tabel dan gambar (opsional; pakai hanya bila memperjelas argumen; tidak dihitung dalam 1.000 kata)

| No | Ketentuan | Ditegakkan oleh |
|---|---|---|
| G1 | Tabel bernomor berurutan; judul + nomor di ATAS tabel, tebal 10 pt ("Tabel 1. Judul") | build |
| G2 | Tabel di tengah halaman/kolom; setelah tabel ada spasi baris 12 pt | build |
| G3 | Isi tabel spasi tunggal (spasi ganda hanya untuk pengelompokan data) | build |
| G4 | Tanpa garis vertikal; hanya garis horizontal (atas, di bawah baris kepala, bawah) | build |
| G5 | Tabel dirujuk di teks dengan nomor SAJA, tanpa kata lokasi ("di atas", "di bawah", "berikut", dll.): benar "Tabel 1", salah "tabel berikut" | check |
| G6 | Gambar bernomor mulai 1; judul + nomor di BAWAH gambar ("Gambar 1. Judul") | build |
| G7 | Gambar jelas, terbaca dengan huruf yang diketik; hitam-putih atau berwarna boleh; gambar dua kolom ditaruh di atas/bawah halaman; ilustrasi cetak dipindai; bila tak bisa dipindai, asli ditempatkan di lokasi | manual |
| G8 | Hanya gambar milik sendiri/bebas hak cipta; jangan menjiplak gambar dari sumber tanpa izin dan rujukan | manual |

## H. Simpulan, ucapan terima kasih

| No | Ketentuan | Ditegakkan oleh |
|---|---|---|
| H1 | Hanya menjawab tujuan penulisan di akhir Pendahuluan | manual |
| H2 | Jelaskan bagaimana argumen memperjelas pemahaman topik di bidang prodi; beri justifikasi jelas, kemungkinan penerapan, dan saran kajian lanjutan | manual |
| H3 | Jangan mengulang abstrak; jangan menambah sumber atau gagasan baru (tanpa sitasi) | check (sitasi) + manual |
| H4 | Satu paragraf, 80–100 kata | check |
| H5 | Ucapan terima kasih opsional; sebut pihak yang membantu (dosen pengampu, pembimbing, korektor); JANGAN menulis nama penulis | check (peringatan) |

## I. Daftar pustaka dan sitasi

| No | Ketentuan | Ditegakkan oleh |
|---|---|---|
| I1 | Hanya memuat sumber yang diacu di teks; semua sitasi teks ada di daftar | check |
| I2 | Kemutakhiran: 10 tahun terakhir | check |
| I3 | Minimal 15 referensi; ≥ 80% sumber primer (artikel riset) | check |
| I4 | Gaya APA 7th; disusun alfabetis (build mengurutkan otomatis); indentasi menggantung | build |
| I5 | Seluruh rujukan nyata dan dapat ditelusuri (DOI atau tautan); rujukan fiktif atau tak tertelusuri = pelanggaran etika akademik | check (`verified`) + manual |
| I6 | Sitasi dalam teks (Penulis, Tahun); parafrase dengan kalimat sendiri; kutipan langsung seperlunya, diberi tanda kutip dan rujukan | check + manual |
| I7 | Disarankan memakai Mendeley Desktop (sebut di pesan penutup: berkas ini dapat diimpor/disinkronkan bila pengguna ingin) | manual |
| I8 | Template mengizinkan sumber "nasional dan internasional"; PERMINTAAN PENGGUNA lebih ketat: semua sumber berbahasa Indonesia | check (`bahasa: id`) |

## J. Hal yang tidak boleh terjadi

- Rujukan dari ingatan/halusinasi, DOI tebakan, tahun/jurnal/halaman dikira-kira.
- Teks petunjuk template tersisa di artikel; nama penulis tetap "Penulis".
- Klaim dalam artikel yang tidak didukung halaman sumber yang benar-benar dibuka.
- Kata "saya"; opini tanpa dukungan; data lapangan buatan.
