# Mencari dan memverifikasi sumber berbahasa Indonesia

## Fakta lingkungan yang sudah diuji (jangan buang waktu mengulang)

- Shell/Bash TIDAK dapat mengakses internet (curl ke Crossref, DOAJ, Garuda, doi.org → 403). Jangan menulis skrip verifikasi online.
- WebFetch hanya membuka URL yang muncul di hasil WebSearch (atau yang diberikan pengguna). URL buatan sendiri, mis. `https://doi.org/...` atau pencarian Garuda `.../documents?q=...`, ditolak (`URL_NOT_ON_ALLOWLIST`). Jangan diulang.
- Jadi alurnya selalu: **WebSearch → ambil tautan dari hasil → WebFetch halaman artikel → catat metadata dari halaman itu**.
- Halaman artikel jurnal OJS (`.../index.php/<jurnal>/article/view/<id>`) terbukti terbaca dan memuat judul, penulis, volume, nomor, halaman, DOI.

## Kriteria sumber yang diterima

1. **Bahasa Indonesia**: judul, abstrak utama, dan isi artikel berbahasa Indonesia (abstrak ganda Indonesia/Inggris boleh). Artikel berjudul Inggris dari jurnal Indonesia DITOLAK.
2. **Terbit ≥ tahun_sekarang − 10** (untuk 2026: 2016 atau lebih baru). Utamakan 5 tahun terakhir.
3. **Artikel riset di jurnal ilmiah** (primer) minimal 80% dari seluruh rujukan. Sisanya boleh buku ajar, artikel telaah, regulasi/pedoman resmi (mis. PUEBI, KBBI daring, peraturan menteri).
4. Punya **DOI** atau tautan halaman artikel yang stabil.
5. Jurnal bereputasi: utamakan terakreditasi SINTA (S1–S4) atau terindeks Garuda; tanda: halaman "About/Akreditasi" jurnal menyebut SINTA.
6. Tidak diterima: Wikipedia, blog, makalah tanpa penulis/tahun, Scribd/Academia unggahan tanpa halaman jurnal, situs jual-beli makalah, artikel di jurnal yang jelas predator.

## Strategi pencarian

- Kueri berbahasa Indonesia, 3–6 kata, variasikan: `<konsep> mahasiswa jurnal`, `<konsep> <program studi> pdf`, `kajian literatur <konsep>`, `<konsep> <tahun>`.
- Perluas dengan istilah Indonesia: `studi pustaka`, `tinjauan literatur`, `pengaruh`, `implementasi`, `strategi`, `analisis`, `persepsi`.
- Tambahkan nama platform: `ejournal`, `jurnal`, `journal` + `ac.id`, atau gunakan parameter `allowed_domains` bila didukung (mis. `ac.id`, `or.id`, `go.id`).
- Jurnal UNRI dan jurnal prodi sendiri dulu (`jurnal.unri.ac.id`), lalu portal OJS kampus lain (UPI, UM, UNJ, UNP, Undiksha, UNS, UNY, UGM, UI, Unair, USU, UIN).
- Untuk tiap konsep di kerangka cari 3–5 kandidat; pilih yang paling relevan dengan klaim.
- Gunakan `mode: "standard"` dahulu; pakai `extended` hanya bila hasil tipis.

## Prosedur verifikasi tiap rujukan (wajib)

1. Ambil tautan artikel dari hasil WebSearch. Bila hasil berupa PDF unduhan (`/article/download/...`), cari juga halaman `view` artikelnya, atau fetch PDF-nya dan baca halaman pertama.
2. WebFetch dengan prompt persis:
   > "Berikan judul lengkap artikel, nama semua penulis (urutan persis), tahun terbit, nama jurnal, volume, nomor, halaman, DOI persis seperti tertulis di halaman, bahasa artikel, dan apakah artikel riset (ada metode/hasil) atau telaah. Sertakan 2–3 kalimat inti isi/abstrak dengan kata-kata Anda sendiri."
3. Salin metadata ke `article.json` HANYA dari hasil fetch. Nama penulis ditulis format APA ("Andriani, D."; inisial dari nama depan/tengah). Bila halaman tidak memuat suatu bagian (mis. halaman), tinggalkan kosong — jangan menebak.
4. Cek silang: judul + penulis pertama + tahun harus sama dengan snippet hasil pencarian. Bila beda → buang atau fetch ulang.
5. Isi: `bahasa: "id"`, `verified: true`, `verified_url` (halaman yang dibuka), `verified_on` (tanggal hari ini, YYYY-MM-DD), `klaim` (1 kalimat: gagasan apa dalam artikel yang didukung rujukan ini), `type`.
6. DOI: hanya yang tertulis di halaman. Tanpa DOI → isi `url` dengan tautan halaman artikel.
7. Rujukan yang tidak bisa dibuka/dicocokkan = dibuang. Jangan "mengisi" dari ingatan.

## Menulis dari sumber tanpa menjiplak

- Baca abstrak/inti yang dikembalikan fetch; tulis ulang dengan struktur kalimat sendiri; dukung klaim hanya sebatas yang ada pada halaman.
- Kutipan langsung: hindari. Bila perlu, satu frasa pendek dalam tanda kutip dengan (Penulis, Tahun, hlm. n) — hlm. hanya bila terbaca.
- Bandingkan: cari minimal satu titik di mana dua sumber sejalan dan satu di mana berbeda/berbeda konteks (untuk komponen F5c).

## Jumlah target

Kumpulkan 20–24 kandidat → verifikasi → simpan 17–20 rujukan (minimal 15), ≥ 80% artikel riset. Semua harus tersitasi di teks.
