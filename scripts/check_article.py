#!/usr/bin/env python3
"""Periksa article.json terhadap ketentuan Template Artikel Konseptual (Universitas Riau).

Pemakaian:
    python3 check_article.py article.json            # periksa
    python3 check_article.py article.json --sitasi   # tampilkan bentuk sitasi tiap rujukan

Keluaran: daftar GAGAL (harus diperbaiki) dan PERINGATAN (periksa manual). Kode keluar 1 bila ada GAGAL.
"""
import datetime
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from artikel_common import (BATAS, TIPE_PRIMER, all_text_blocks, cite_forms,  # noqa: E402
                            count_words, strip_md, surname)

SISA_TEMPLATE = [
    "Template ini dirancang", "Tempel Khusus", "Nama Program Studi", "Nama Perguruan Tinggi",
    "Email Penulis", "Judul Lugas", "Kata kunci berisi", "Abstracts are written",
    "Hapus seluruh teks petunjuk", "[Topik]", "[Masalah]", "[Konsep A]", "Mendeley Desktop",
    "Ketentuan artikel konseptual", "Komponen berikut harus",
]
PLACEHOLDER = re.compile(r"\[(Nama Penulis|email|Nama|Isi|ISI|TODO)[^\]]*\]", re.I)
KATA_PERSONAL = re.compile(r"\b(saya|aku|gue|gua)\b", re.I)
KATA_KITA = re.compile(r"\b(kita|kami|kamu|anda)\b", re.I)
KATA_INFORMAL = re.compile(r"\b(nggak|gak|banget|bikin|cuma|udah|emang|kayak|gimana)\b", re.I)
MUBAZIR = [
    "adalah merupakan", "agar supaya", "demi untuk", "seperti misalnya", "sangat sekali",
    "disebabkan karena", "bahwasanya", "serta juga", "dan lain sebagainya dll", "hanya saja",
    "para ... -para", "dapat bisa", "sebagai contohnya misalnya", "kemudian lalu",
    "oleh karena itu maka", "walaupun demikian tetapi", "meskipun begitu namun",
]
LOKASI_TABEL = re.compile(r"\b(tabel|gambar)\s+(di\s+atas|di\s+bawah|berikut|ini|tersebut)\b", re.I)
SITASI_PAR = re.compile(r"\(([^()]*?(?:19|20)\d\d[a-z]?(?:\s*;\s*[^()]*?(?:19|20)\d\d[a-z]?)*)\)")
SITASI_NAR = re.compile(r"([A-Z][\w'’\-]+(?:\s+(?:&|dan)\s+[A-Z][\w'’\-]+|\s+\*?et al\.\*?)?)\s+\(((?:19|20)\d\d[a-z]?)\)")
ID_STOP = set("yang dan di untuk pada dengan dalam dari ini itu adalah terhadap oleh atau sebagai secara juga tidak ke bagi antara serta dapat akan".split())
EN_STOP = set("the of and in for to with on from by is are as an at or be this that using study analysis effect between".split())
EN_ISTILAH = set("learning online offline blended skill skills soft hard mindset literacy digital big framework review "
                 "feedback outcome outcomes design based project problem teaching teacher student students engagement "
                 "critical thinking creative creativity machine deep content curriculum assessment".split())


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    with open(args[0], encoding="utf-8") as f:
        art = json.load(f)

    gagal, warn, info = [], [], []
    tahun_ini = datetime.date.today().year

    def need(cond, msg):
        if not cond:
            gagal.append(msg)

    # ------------------------------------------------ bidang wajib
    for k in ("judul", "penulis", "afiliasi", "email", "abstrak", "kata_kunci", "abstract", "keywords",
              "pendahuluan", "pembahasan", "simpulan", "rujukan"):
        need(art.get(k), f"Bidang wajib kosong/tidak ada: {k}")
    if gagal:
        report(gagal, warn, info)

    # ------------------------------------------------ judul & penulis
    n = count_words(art["judul"])
    need(n <= BATAS["judul_maks_kata"], f"Judul {n} kata (maks {BATAS['judul_maks_kata']}).")
    need(art["penulis"].strip().lower() != "penulis", "Nama penulis masih 'Penulis' (teks template).")
    if "@" not in art["email"]:
        warn.append("Email corresponding author belum terisi/valid.")
    if PLACEHOLDER.search(art["penulis"] + art["email"] + art["afiliasi"]):
        warn.append("Nama/email/afiliasi masih berupa penanda [..]; minta pengguna mengisi.")
    need("riau" in art["afiliasi"].lower() or art["afiliasi"].count(",") >= 1,
         "Afiliasi harus berbentuk 'Program Studi, Perguruan Tinggi'.")

    # ------------------------------------------------ abstrak & kata kunci
    for kunci, nama in (("abstrak", "Abstrak"), ("abstract", "Abstract")):
        txt = art[kunci]
        w = count_words(txt)
        need(BATAS["abstrak_min"] <= w <= BATAS["abstrak_maks"], f"{nama}: {w} kata (harus 100–150).")
        need("\n" not in txt.strip(), f"{nama} harus satu alinea (ada pemisah baris).")
        need(not SITASI_PAR.search(txt) and not SITASI_NAR.search(txt), f"{nama} memuat sitasi (dilarang).")
        need(not re.search(r"\b(Tabel|Gambar|Table|Figure)\s+\d", txt), f"{nama} memuat rujukan tabel/gambar (dilarang).")
        need("=" not in txt, f"{nama} memuat tanda persamaan (dilarang).")
    for kunci, nama in (("kata_kunci", "Kata kunci"), ("keywords", "Keyword")):
        need(1 <= len(art[kunci]) <= BATAS["kata_kunci_maks"], f"{nama}: {len(art[kunci])} butir (maks 5).")
        need(not any(";" in k for k in art[kunci]), f"{nama}: jangan isi butir dengan titik koma; pisahkan per elemen larik.")
    need(len(art["kata_kunci"]) == len(art["keywords"]), "Jumlah kata kunci dan keyword harus sama.")

    # ------------------------------------------------ jumlah kata isi
    blok = all_text_blocks(art)
    w_pend = sum(count_words(p) for p in blok["pendahuluan"])
    w_pemb = sum(count_words(p) for p in blok["pembahasan"])
    w_head = sum(count_words(h) for h in blok["pembahasan_subjudul"])
    w_sim = sum(count_words(p) for p in blok["simpulan"])
    total = w_pend + w_pemb + w_sim
    info.append(f"Kata: Pendahuluan {w_pend} | Pembahasan {w_pemb} (+{w_head} kata subjudul) | Simpulan {w_sim} | Total {total}")
    need(BATAS["pendahuluan"][0] <= w_pend <= BATAS["pendahuluan"][1], f"Pendahuluan {w_pend} kata (target 250–350).")
    need(BATAS["pembahasan"][0] <= w_pemb and w_pemb + w_head <= BATAS["pembahasan"][1],
         f"Pembahasan {w_pemb} kata + {w_head} kata subjudul (target 700–900 termasuk subjudul; paragraf saja ≥ 700).")
    need(BATAS["simpulan"][0] <= w_sim <= BATAS["simpulan"][1], f"Simpulan {w_sim} kata (target 80–100).")
    need(total >= BATAS["total_min"], f"Total Pendahuluan–Simpulan {total} kata (minimal 1.000).")
    need(not isinstance(art["simpulan"], list), "Simpulan harus SATU paragraf (string), bukan larik.")

    subs = art["pembahasan"].get("subjudul", [])
    need(BATAS["subjudul"][0] <= len(subs) <= BATAS["subjudul"][1], f"Pembahasan punya {len(subs)} subjudul (harus 3–5).")
    if len(art["pendahuluan"]) < 2:
        warn.append("Pendahuluan hanya 1 paragraf; template: latar belakang (maks 1 paragraf) + tinjauan literatur singkat + tujuan.")

    # ------------------------------------------------ rujukan
    refs = art["rujukan"]
    need(len(refs) >= BATAS["rujukan_min"], f"Rujukan {len(refs)} (minimal 15).")
    batas_tahun = tahun_ini - BATAS["rentang_tahun"]
    n_primer = 0
    for i, r in enumerate(refs, 1):
        tag = f"Rujukan #{i} ({'; '.join(surname(a) for a in r.get('authors', []))} {r.get('year', '?')})"
        for k in ("authors", "year", "title", "type"):
            need(r.get(k), f"{tag}: bidang '{k}' kosong.")
        if r.get("type") in ("artikel-riset", "artikel-telaah"):
            need(r.get("journal"), f"{tag}: nama jurnal kosong.")
        if r.get("type") == "buku":
            need(r.get("publisher"), f"{tag}: nama penerbit buku kosong.")
        if r.get("type") in TIPE_PRIMER:
            n_primer += 1
        try:
            need(int(r["year"]) >= batas_tahun, f"{tag}: terbit {r['year']}, lebih tua dari 10 tahun (≥ {batas_tahun}).")
            need(int(r["year"]) <= tahun_ini, f"{tag}: tahun {r['year']} melewati tahun sekarang.")
        except (KeyError, ValueError):
            gagal.append(f"{tag}: tahun tidak valid.")
        doi = (r.get("doi") or "").strip()
        url = (r.get("url") or "").strip()
        need(doi or url, f"{tag}: tidak ada DOI maupun URL (wajib dapat ditelusuri).")
        if doi:
            d = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi)
            need(re.match(r"^10\.\d{4,9}/\S+$", d), f"{tag}: format DOI tidak valid: {doi}")
        need(r.get("bahasa") == "id", f"{tag}: bahasa sumber harus 'id' (sumber wajib berbahasa Indonesia).")
        need(r.get("verified") is True and r.get("verified_url") and r.get("verified_on"),
             f"{tag}: belum terverifikasi (verified=true, verified_url, verified_on wajib diisi setelah halaman sumber dibuka).")
        need(r.get("klaim"), f"{tag}: isi 'klaim' (apa yang didukung rujukan ini) agar tidak ada sitasi kosong.")
        # bahasa judul (heuristik)
        toks = re.findall(r"[a-zA-Z]+", r.get("title", "").lower())
        idn, eng = sum(t in ID_STOP for t in toks), sum(t in EN_STOP for t in toks)
        if eng > idn and eng >= 2:
            warn.append(f"{tag}: judul tampak berbahasa Inggris — sumber harus berbahasa Indonesia.")
        # sentence case (APA 7)
        kata = [t for t in r.get("title", "").split() if t.isalpha() and t.lower() not in ID_STOP | EN_STOP]
        if len(kata) >= 4 and sum(t[0].isupper() for t in kata[1:]) / max(1, len(kata) - 1) > 0.6:
            warn.append(f"{tag}: judul artikel tampak Title Case; APA 7 memakai huruf besar hanya di awal kalimat/nama diri.")
    if refs:
        share = n_primer / len(refs)
        info.append(f"Sumber primer (artikel riset): {n_primer}/{len(refs)} = {share:.0%}")
        need(share >= BATAS["primer_min"], f"Sumber primer {share:.0%} (< 80%).")
    kunci = [(surname(r["authors"][0]).lower(), str(r["year"]) + r.get("year_suffix", "")) for r in refs if r.get("authors")]
    dup = {k for k in kunci if kunci.count(k) > 1}
    for d in dup:
        need(False, f"Dua rujukan dengan penulis pertama '{d[0]}' dan tahun '{d[1]}' sama: beri year_suffix a/b dan bedakan di teks.")

    # ------------------------------------------------ silang sitasi <-> daftar pustaka
    teks_isi = "\n".join(blok["pendahuluan"] + blok["pembahasan"] + blok["simpulan"])
    cited_keys = set()
    for m in SITASI_PAR.finditer(teks_isi):
        for bagian in m.group(1).split(";"):
            mm = re.search(r"([A-Z][\w'’\-]+).*?((?:19|20)\d\d[a-z]?)\s*$", bagian.strip())
            if mm:
                cited_keys.add((mm.group(1).lower(), mm.group(2)))
    for m in SITASI_NAR.finditer(teks_isi):
        cited_keys.add((m.group(1).split()[0].lower(), m.group(2)))
    ref_keys = {(surname(r["authors"][0]).lower().split()[0], str(r["year"]) + r.get("year_suffix", "")) for r in refs if r.get("authors")}
    for s, y in sorted(cited_keys - ref_keys):
        need(False, f"Sitasi ({s.title()}, {y}) tidak ada di daftar pustaka.")
    for s, y in sorted(ref_keys - cited_keys):
        need(False, f"Rujukan {s.title()} ({y}) ada di daftar pustaka tetapi tidak disitasi di teks.")
    sit_sim = SITASI_PAR.search(art["simpulan"]) or SITASI_NAR.search(art["simpulan"])
    need(not sit_sim, "Simpulan memuat sitasi (tidak boleh menambah sumber/gagasan baru).")
    info.append(f"Sitasi unik di teks: {len(cited_keys)}")

    # ------------------------------------------------ kaidah bahasa
    semua = "\n".join([art["abstrak"]] + blok["pendahuluan"] + blok["pembahasan"] + blok["simpulan"]
                      + [art.get("ucapan_terima_kasih", "")])
    polos = strip_md(semua)
    need(not KATA_PERSONAL.search(polos), f"Kata orang pertama dilarang (saya/aku): {sorted(set(m.group(0).lower() for m in KATA_PERSONAL.finditer(polos)))}")
    if KATA_KITA.search(polos):
        warn.append(f"Kata kita/kami/Anda ditemukan; gunakan kalimat objektif: {sorted(set(m.group(0).lower() for m in KATA_KITA.finditer(polos)))}")
    if KATA_INFORMAL.search(polos):
        need(False, f"Kata tidak baku: {sorted(set(m.group(0).lower() for m in KATA_INFORMAL.finditer(polos)))}")
    for frasa in MUBAZIR:
        if frasa in polos.lower():
            warn.append(f"Kemungkinan kata mubazir: '{frasa}'.")
    if re.search(r"\bdkk\.?", polos):
        warn.append("Ditemukan 'dkk.'; pakai '*et al.*' (miring) agar konsisten dengan APA 7th.")
    for m in LOKASI_TABEL.finditer(polos):
        need(False, f"Rujukan tabel/gambar tidak boleh memakai kata lokasi: '{m.group(0)}' (tulis 'Tabel 1').")
    for i, sub in enumerate(subs, 1):
        if sub.get("tabel"):
            need(re.search(rf"\bTabel {sum(1 for s in subs[:i] if s.get('tabel'))}\b", teks_isi), f"Tabel pada subjudul {i} tidak dirujuk di teks (mis. 'Tabel 1').")
        if sub.get("gambar"):
            need(re.search(rf"\bGambar {sum(1 for s in subs[:i] if s.get('gambar'))}\b", teks_isi), f"Gambar pada subjudul {i} tidak dirujuk di teks.")
    # bahasa umum
    toks = re.findall(r"[a-zA-Z]+", polos.lower())
    if sum(t in EN_STOP for t in toks) > sum(t in ID_STOP for t in toks) * 0.3:
        warn.append("Banyak kata Inggris di teks isi; tulis dalam bahasa Indonesia baku.")
    # istilah asing harus miring
    tanpa_miring = re.sub(r"\*[^*]+\*", " ", semua)
    asing = sorted({t for t in re.findall(r"[A-Za-z]+", tanpa_miring.lower()) if t in EN_ISTILAH})
    if asing:
        warn.append(f"Istilah asing yang belum miring (periksa & beri *tanda bintang*): {asing}")
    # sisa teks template
    seluruh = json.dumps(art, ensure_ascii=False)
    for s in SISA_TEMPLATE:
        need(s not in seluruh, f"Sisa teks petunjuk template ditemukan: '{s}'")
    ucap = art.get("ucapan_terima_kasih", "").lower()
    nama_tok = [t for t in re.findall(r"[A-Za-z]+", art["penulis"].lower()) if len(t) >= 4]
    if ucap and any(re.search(rf"\b{re.escape(t)}\b", ucap) for t in nama_tok):
        warn.append("Ucapan terima kasih tampak memuat nama penulis; template melarangnya.")
    # paragraf satu gagasan
    for nama, ps in (("Pendahuluan", blok["pendahuluan"]), ("Pembahasan", blok["pembahasan"])):
        for j, p in enumerate(ps, 1):
            kal = len(re.findall(r"[.!?](\s|$)", strip_md(p)))
            if kal > 9:
                warn.append(f"{nama} paragraf {j}: {kal} kalimat; pecah agar satu paragraf = satu gagasan pokok.")
    # tujuan di akhir pendahuluan
    akhir = strip_md(blok["pendahuluan"][-1]).lower() if blok["pendahuluan"] else ""
    if not re.search(r"(tujuan|bertujuan|dimaksudkan|bermaksud)", akhir[-400:]):
        warn.append("Paragraf terakhir Pendahuluan belum memuat kalimat tujuan penulisan (kata 'tujuan/bertujuan').")
    if "--sitasi" in sys.argv:
        for r in sorted(refs, key=lambda x: (surname(x['authors'][0]).lower(), str(x['year']))):
            par, nar = cite_forms(r)
            print(f"{par:45s} | {nar}")
    report(gagal, warn, info)


def report(gagal, warn, info):
    for i in info:
        print("INFO     ", i)
    for w in warn:
        print("PERINGATAN", w)
    for g in gagal:
        print("GAGAL    ", g)
    print(f"\nRingkasan: {len(gagal)} GAGAL, {len(warn)} PERINGATAN")
    sys.exit(1 if gagal else 0)


if __name__ == "__main__":
    main()
