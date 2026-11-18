# APA 7th untuk sumber berbahasa Indonesia

build_docx.py membentuk daftar pustaka otomatis dari bidang terstruktur, jadi yang penting ialah mengisi bidang dengan benar.

## Nama penulis (bidang `authors`)

Format "Nama belakang, Inisial." per orang.
- Andriani, D. | Abdulkarim, A. | Insani, N. N.
- Nama Indonesia satu kata (mis. "Suharto"): tulis "Suharto" tanpa inisial (APA 7: nama tunggal ditulis utuh). Nama dengan beberapa kata: umumnya nama terakhir sebagai nama belakang kecuali penulis/jurnal memakai bentuk lain; ikuti bentuk di halaman artikel.
- Penulis lembaga: satu elemen, mis. "Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi".
- Daftar akhir otomatis: 1 penulis `A`; 2 penulis `A, & B`; 3+ penulis `A, B, & C`.

## Judul (bidang `title`)

Judul artikel/buku: huruf besar hanya pada huruf pertama, setelah titik dua, dan nama diri (sentence case).
- Benar: "Implementasi program Kampus Mengajar dalam pembentukan karakter tanggung jawab mahasiswa"
- Salah: "Implementasi Program Kampus Mengajar Dalam Pembentukan Karakter ..."
Nama jurnal tetap Title Case dan akan dimiringkan otomatis.

## Contoh hasil

Artikel jurnal:
Andriani, D., Abdulkarim, A., & Insani, N. N. (2023). Implementasi program Kampus Mengajar dalam pembentukan karakter tanggung jawab mahasiswa. *Jurnal Ilmiah Mimbar Demokrasi*, *23*(1), 273–284. https://doi.org/10.21009/jimd.v23i1.37963

Buku (`type: buku`, bidang `edition`, `publisher`):
Penulis, A. (2020). *Judul buku dengan huruf kecil* (Edisi ke-2). Penerbit.

## Sitasi dalam teks

| Jumlah penulis | Dalam kurung | Naratif |
|---|---|---|
| 1 | (Andriani, 2023) | Andriani (2023) |
| 2 | (Andriani & Insani, 2023) | Andriani dan Insani (2023) |
| 3+ | (Andriani *et al.*, 2023) | Andriani *et al.* (2023) |

- Beberapa sumber sekaligus: urut alfabet, pisah titik koma — (Andriani *et al.*, 2023; Pratama, 2021).
- `et al.` dimiringkan (istilah asing). Jangan campur dengan "dkk.".
- Dua rujukan dengan penulis pertama dan tahun sama: beri `year_suffix` "a"/"b" → (Pratama, 2021a).
- Kutipan langsung (jarang): "kalimat pendek" (Penulis, Tahun, hlm. 5).
- Perintah `python3 check_article.py article.json --sitasi` menampilkan bentuk sitasi tiap rujukan agar tidak salah ketik.
