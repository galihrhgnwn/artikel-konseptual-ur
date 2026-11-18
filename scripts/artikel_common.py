#!/usr/bin/env python3
"""Fungsi bersama untuk build_docx.py dan check_article.py.

Penanda teks di article.json:
  *miring*   -> huruf miring (istilah asing, nama jurnal di daftar pustaka)
  **tebal**  -> huruf tebal
"""
import re

BATAS = {
    "judul_maks_kata": 12,
    "abstrak_min": 100, "abstrak_maks": 150,
    "kata_kunci_maks": 5,
    "pendahuluan": (250, 350),
    "pembahasan": (700, 900),
    "subjudul": (3, 5),
    "simpulan": (80, 100),
    "total_min": 1000,
    "rujukan_min": 15,
    "primer_min": 0.80,
    "rentang_tahun": 10,
}

TIPE_PRIMER = {"artikel-riset", "prosiding-riset"}


def strip_md(text):
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    return text


def count_words(text):
    """Hitung kata seperti penghitung kata Word: pisah spasi, abaikan token tanpa huruf/angka."""
    return len([t for t in strip_md(text).split() if re.search(r"\w", t)])


def surname(author):
    return author.split(",")[0].strip()


def format_authors(authors):
    a = [x.strip() for x in authors]
    if not a:
        return ""
    if len(a) == 1:
        return a[0]
    if len(a) == 2:
        return f"{a[0]}, & {a[1]}"
    return ", ".join(a[:-1]) + f", & {a[-1]}"


def doi_url(ref):
    doi = (ref.get("doi") or "").strip()
    if doi:
        doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi)
        return f"https://doi.org/{doi}"
    return (ref.get("url") or "").strip()


def format_reference(ref):
    """Kembalikan satu entri daftar pustaka gaya APA 7th (dengan penanda *miring*)."""
    au = format_authors(ref["authors"])
    yr = f"({ref['year']}{ref.get('year_suffix', '')})"
    head = f"{au} {yr}." if not au.endswith(".") else f"{au} {yr}."
    link = doi_url(ref)
    tipe = ref.get("type", "artikel-riset")
    if tipe in ("artikel-riset", "artikel-telaah"):
        vol = ref.get("volume", "")
        iss = ref.get("issue", "")
        pages = ref.get("pages", "")
        src = f"*{ref['journal']}*"
        if vol:
            src += f", *{vol}*"
            if iss:
                src += f"({iss})"
        if pages:
            src += f", {pages}"
        body = f"{ref['title']}. {src}."
    elif tipe == "buku":
        ed = f" ({ref['edition']})" if ref.get("edition") else ""
        pub = ref.get("publisher", "").strip()
        body = f"*{ref['title']}*{ed}." + (f" {pub}." if pub else "")
    else:  # prosiding-riset, laporan, regulasi, web
        src = ref.get("journal") or ref.get("publisher") or ""
        body = f"*{ref['title']}*." + (f" {src}." if src else "")
    out = f"{head} {body}"
    if link:
        out += f" {link}"
    return out


def sort_key(ref):
    names = [surname(a).lower() for a in ref["authors"]]
    return (names, str(ref["year"]) + ref.get("year_suffix", ""))


def cite_forms(ref):
    """Bentuk sitasi dalam teks (APA 7th) untuk satu rujukan."""
    n = len(ref["authors"])
    s = [surname(a) for a in ref["authors"]]
    yr = f"{ref['year']}{ref.get('year_suffix', '')}"
    if n == 1:
        par, nar = f"{s[0]}, {yr}", f"{s[0]} ({yr})"
    elif n == 2:
        par, nar = f"{s[0]} & {s[1]}, {yr}", f"{s[0]} dan {s[1]} ({yr})"
    else:
        par, nar = f"{s[0]} *et al.*, {yr}", f"{s[0]} *et al.* ({yr})"
    return f"({par})", nar


def all_text_blocks(art):
    """Semua paragraf isi (Pendahuluan–Simpulan) untuk pemeriksaan."""
    blocks = {"pendahuluan": list(art.get("pendahuluan", []))}
    pemb = art.get("pembahasan", {})
    paras = list(pemb.get("pengantar", []))
    heads = []
    for sec in pemb.get("subjudul", []):
        heads.append(sec.get("judul", ""))
        paras += sec.get("paragraf", [])
    blocks["pembahasan"] = paras
    blocks["pembahasan_subjudul"] = heads
    sim = art.get("simpulan", "")
    blocks["simpulan"] = [sim] if sim else []
    return blocks
