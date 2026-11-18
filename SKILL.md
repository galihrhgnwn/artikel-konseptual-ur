---
name: artikel-konseptual-ur
description: Menulis artikel konseptual baru (telaah literatur tanpa data lapangan), atau merevisi artikel yang sudah ada agar sesuai template, untuk Mata Kuliah Bahasa Indonesia Universitas Riau. Semua rujukan berbahasa Indonesia, dicari dan diverifikasi lewat alat web, gaya APA 7th, abstrak dwibahasa, keluaran .docx berformat template (Lato, header/footer). Gunakan saat pengguna meminta artikel konseptual, artikel ilmiah, atau tugas artikel Bahasa Indonesia berdasarkan template Universitas Riau.
---

# Artikel Konseptual — Bahasa Indonesia, Universitas Riau

Menghasilkan satu berkas .docx yang memenuhi seluruh ketentuan template: SATU argumen utama dibela sepanjang tulisan, disusun dari telaah literatur, tanpa data lapangan. Dua mode: **artikel baru** dan **revisi artikel yang sudah ada** (lihat "Langkah 0").

## Aturan yang tidak boleh dilanggar

1. **Rujukan nyata, berbahasa Indonesia, terbuka dan terverifikasi.** Setiap rujukan harus lahir dari halaman sumber yang benar-benar dibuka lewat alat web pada sesi ini. Dilarang menulis rujukan, DOI, tahun, volume, atau halaman dari ingatan. Rujukan yang tidak bisa diverifikasi dibuang.
2. Rujukan: minimal 15 (target 17–20), ≥ 80% artikel riset, terbit 10 tahun terakhir, semua tersitasi di teks.
3. Satu argumen utama; tujuan di akhir Pendahuluan; Simpulan hanya menjawab tujuan itu.
4. Tanpa kata "saya"; kalimat efektif, objektif, baku; istilah asing miring; satu paragraf satu gagasan.
4a. **Bagian bahasa Inggris selalu miring**: seluruh isi *Abstract* dan isi *Keyword* ditulis huruf miring (otomatis oleh `build_docx.py`); label "Keyword:" tebal tegak. Isi "Kata Kunci" juga miring.
5. Parafrase penuh; klaim hanya sebatas yang didukung halaman sumber yang dibuka.
6. Angka kata dihitung dengan skrip, bukan perkiraan. Berkas tidak diserahkan sebelum `check_article.py` bersih dari GAGAL.
7. Penulis tetap bertanggung jawab atas isi dan rujukan: ingatkan pengguna membuka DOI/tautan sendiri.

Daftar lengkap ketentuan template (± 70 butir kecil, dengan penanda siapa yang menegakkan): `references/template-ketentuan.md`. Baca sebelum menulis.

## Alat yang dibutuhkan

- Pencarian web + pembuka halaman (WebSearch, WebFetch). Tanpa ini, katakan terus terang bahwa rujukan tidak bisa diverifikasi dan jangan membuat rujukan.
- Python 3 + `python-docx` (membangun .docx). `soffice` + `pdftoppm` opsional untuk pratinjau.
- Shell biasanya TIDAK punya akses internet; jangan mencoba curl/pip. Detail dan cara kerja yang sudah teruji: `references/sumber-indonesia.md`.

## Langkah 0 — Tanya: artikel baru atau revisi?

Pertanyaan PERTAMA, sebelum apa pun (pakai polling, mis. AskUserQuestion, bila tersedia; bila tidak, tanya biasa):

> "Sudah ada artikel sebelumnya yang mau direvisi, atau mau buat artikel baru dari awal?"
> Pilihan: **Buat artikel baru** | **Revisi artikel yang sudah ada**

- **Artikel baru** → lanjut ke "Alur kerja" di bawah.
- **Revisi** → minta pengguna mengirim artikel sebelumnya (.docx lebih baik; .pdf atau teks tempel juga boleh) dan, bila ada, catatan/komentar dosen atau permintaan perubahan khusus. Jangan mulai sebelum berkasnya ada. Lalu ikuti "Alur revisi".
- Bila pengguna sudah jelas menyebut salah satunya di pesan pertama, jangan bertanya lagi.

## Alur revisi (artikel lama → sesuai template)

Tujuan: memperbaiki artikel pengguna agar memenuhi seluruh ketentuan template, TANPA menggantinya menjadi tulisan lain.

1. **Baca berkasnya** (.docx: ekstrak teks dengan python-docx atau skill docx; .pdf: pdftotext; sertakan tabel/gambar). Bila ada komentar dosen, catat sebagai daftar perbaikan wajib.
2. **Salin ke `article.json`** apa adanya (belum diubah): judul, penulis, afiliasi, abstrak, Pendahuluan, Pembahasan (+ subjudul), Simpulan, ucapan terima kasih, daftar pustaka dipecah ke bidang terstruktur. Tandai istilah asing dengan `*miring*`. Isi `penulis`, `afiliasi`, `email`, kelas dari berkas lama; tanya hanya yang tidak ada.
3. **Audit**: jalankan `scripts/check_article.py` pada JSON itu, lalu bandingkan manual dengan `references/template-ketentuan.md`. Susun daftar temuan (jumlah kata per bagian, abstrak, struktur Pendahuluan, subjudul, komponen Pembahasan F5 a–c, Simpulan, tabel/gambar, sitasi vs daftar pustaka, kaidah bahasa, format).
4. **Verifikasi setiap rujukan lama** lewat WebSearch + WebFetch (`references/sumber-indonesia.md`). Rujukan yang nyata dan memenuhi syarat dipertahankan dan diisi metadata verifikasinya. Yang fiktif, tidak ditemukan, berbahasa Inggris, lebih tua dari 10 tahun, atau tidak cocok dengan klaimnya DIGANTI dengan sumber baru yang terverifikasi, dan beri tahu pengguna satu per satu. Pastikan ≥ 15 rujukan dan ≥ 80% artikel riset.
5. **Perbaiki seperlunya** (prinsip perubahan minimal):
   - Pertahankan argumen utama, gagasan, urutan, dan gaya penulis pengguna. Ubah hanya yang melanggar template atau komentar dosen.
   - Bagian kurang kata → tambah isi yang didukung sumber; kelebihan → ringkas bagian yang paling tidak mendukung argumen.
   - Susun ulang bagian yang salah tempat (mis. ringkasan hasil di Pendahuluan, sumber baru di Simpulan, "A menyatakan…, B menyatakan…" → dikelompokkan per topik).
   - Tambahkan bagian yang hilang (abstrak Inggris, kata kunci, tujuan di akhir Pendahuluan, bandingan sumber di Pembahasan).
   - Perbaiki ejaan, kalimat tidak efektif, kata "saya", istilah asing tanpa miring, sitasi tidak sesuai APA 7th.
   - Jangan mengarang data lapangan; jangan menambahkan klaim yang tidak didukung halaman sumber.
6. **Periksa ulang** (`check_article.py` sampai tanpa GAGAL), **bangun** `.docx`, dan **pratinjau** seperti langkah 6–8 alur kerja.
7. **Serahkan** hasil revisi bersama **catatan perubahan** singkat dan jelas: (a) pelanggaran template yang ditemukan dan cara memperbaikinya, (b) rujukan yang dipertahankan, diganti, atau dibuang beserta alasannya, (c) jumlah kata sebelum dan sesudah per bagian, (d) hal yang perlu diputuskan pengguna. Tetap ingatkan pengguna membuka DOI sendiri dan membaca ulang hasil revisi.

## Alur kerja (artikel baru)

1. **Tanya pengguna dulu** (sebelum mencari sumber), hanya data yang belum diketahui dan sesuai isian template. Pakai alat tanya berpilihan (polling, mis. AskUserQuestion) bila tersedia; bila tidak, tanya biasa dalam satu pesan. Jangan menanyakan hal yang sudah disebut pengguna.
   - **Isian ketik bebas** (tanya biasa atau pilihan "Lainnya"): nama penulis, program studi, perguruan tinggi (default Universitas Riau), email corresponding author, kelas untuk header (default: "Kelas E1 Tempuk Manggis 9"), tahun ajaran footer (default: 2026/2027), dan topik.
   - **Isian berpilihan (polling)**: topik (3 usulan sesuai prodi bila pengguna belum punya), pakai Ucapan Terima Kasih atau tidak (bila ya, minta nama dosen pengampu), perlu tabel/gambar atau tidak (default: tidak).
   - Bila pengguna tak menjawab atau data kurang, lanjutkan dengan penanda `[Nama Penulis]` / `[email]` dan beri tahu di pesan penutup.
2. **Rumuskan** argumen utama dan tujuan (satu kalimat tesis; kalimat tujuan: "Tujuan artikel ini ialah …").
3. **Cari dan verifikasi sumber** sesuai `references/sumber-indonesia.md`: kueri berbahasa Indonesia → WebSearch → buka halaman artikel dengan WebFetch → salin metadata dari halaman itu ke `article.json` (`verified`, `verified_url`, `verified_on`, `klaim`). Kumpulkan 20–24 kandidat, simpan 17–20.
4. **Kerangka**: 3–5 subjudul Pembahasan, tiap subjudul dipetakan ke rujukan dan satu bagian argumen; sisipkan satu titik "sumber sejalan" dan satu "sumber berbeda" (komponen F5c).
5. **Tulis** ke `article.json` (skema: `assets/article.example.json`; format sitasi/daftar pustaka: `references/apa7-indonesia.md`). Urutan penulisan yang disarankan: Pembahasan → Pendahuluan → Simpulan → Abstrak → Kata kunci → terjemahan Inggris.
6. **Periksa**: `python3 scripts/check_article.py article.json`. Perbaiki semua GAGAL, telaah setiap PERINGATAN, ulangi sampai bersih. `--sitasi` mencetak bentuk sitasi tiap rujukan.
7. **Bangun**: `python3 scripts/build_docx.py article.json Artikel_<Nama>.docx`.
8. **Pratinjau**: `bash scripts/render_preview.sh Artikel_<Nama>.docx` lalu lihat halaman PNG: header merah + kotak nomor, judul 24 tebal, "✉ Corresponding author", Abstrak/Abstract, subjudul tebal, tabel tanpa garis vertikal, footer gelap. Perbaiki bila ada yang berbeda dari template.
9. **Serahkan** berkas .docx (dan `article.json` bila diminta). Pesan penutup singkat: topik, argumen, jumlah kata per bagian, jumlah rujukan, rujukan yang paling lemah verifikasinya, bagian yang masih harus diisi pengguna (nama/email), catatan font Lato bila tidak terpasang, pengingat membuka DOI sendiri, dan bahwa berkas dapat diimpor ke Mendeley bila ingin.

## Skema `article.json` (ringkas)

- `judul`, `penulis`, `afiliasi` ("Program Studi, Perguruan Tinggi"), `email`
- `abstrak`, `kata_kunci[]`, `abstract`, `keywords[]`
- `pendahuluan[]` (paragraf), `pembahasan.pengantar[]`, `pembahasan.subjudul[]` (`judul`, `paragraf[]`, opsional `tabel{judul,kepala,baris,lebar_cm}` / `gambar{berkas,judul,lebar_cm}`)
- `simpulan` (string, satu paragraf), `ucapan_terima_kasih` (opsional)
- `rujukan[]`: `authors[]` ("Nama, I."), `year`, `title` (sentence case), `journal`/`publisher`, `volume`, `issue`, `pages`, `doi` atau `url`, `type` (`artikel-riset` | `artikel-telaah` | `buku` | `prosiding-riset` | `laporan` | `regulasi`), `bahasa:"id"`, `verified`, `verified_url`, `verified_on`, `klaim`
- Penanda teks: `*miring*`, `**tebal**`. Sitasi: (Penulis, Tahun) / (A & B, Tahun) / (A *et al.*, Tahun).

## Batas angka (diperiksa skrip)

Judul ≤ 12 kata · Abstrak dan Abstract 100–150 kata, satu alinea · Kata kunci ≤ 5 · Pendahuluan 250–350 · Pembahasan 700–900 (dengan 3–5 subjudul) · Simpulan 80–100 · Total Pendahuluan–Simpulan ≥ 1.000 · Rujukan ≥ 15, ≥ 80% primer, ≤ 10 tahun.

## Saat sesuatu tidak bisa dipenuhi

- Sumber berbahasa Indonesia untuk topik terlalu sedikit → persempit/ubah sudut topik, jangan menambah sumber berbahasa Inggris tanpa izin pengguna; tawarkan pilihan bila perlu.
- Alat web tidak tersedia → berhenti di tahap kerangka dan kandidat kata kunci pencarian; katakan jelas bahwa daftar pustaka belum bisa dibuat secara jujur.
- Lato tidak ada di mesin → tetap bernama Lato di berkas; pratinjau memakai Carlito.
