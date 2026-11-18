#!/usr/bin/env python3
"""Bangun artikel .docx sesuai Template Artikel Konseptual (Mata Kuliah Bahasa Indonesia, Universitas Riau).

Pemakaian:
    python3 build_docx.py article.json keluaran.docx

Detail format diukur dari PDF template resmi:
  A4, margin kiri/kanan 2,2 cm, atas 2,2 cm, bawah 2,0 cm; font Lato 11, spasi 1, rata kiri-kanan,
  alinea menjorok 1 cm; header teks merah rata kanan + kotak nomor halaman abu-abu (7F7F7F);
  garis abu-abu (D9D9D9) di bawah header; footer bilah abu gelap (404040), teks putih Arial 9,
  garis biru (4F81BD) di atasnya.
"""
import json
import re
import sys
import os

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from artikel_common import cite_forms, format_reference, sort_key  # noqa: E402

FONT = "Lato"
FONT_ALT = "Arial"
HEADER_DEFAULT = "Artikel Konseptual – Mata Kuliah Bahasa Indonesia Kelas E1 Tempuk Manggis 9"
FOOTER_DEFAULT = "Universitas Riau – Bahasa Indonesia 2026/2027"
LEBAR_TEKS_CM = 16.6
INDENT_CM = 1.0
MARK = "✉"  # simbol amplop penanda corresponding author

TOKEN = re.compile(r"(\*\*.+?\*\*|\*.+?\*)")


# ---------------------------------------------------------------- utilitas level rendah
def set_font(run, size=11, bold=None, italic=None, color=None, name=FONT, superscript=False):
    run.font.name = name
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(attr), name)
    run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    if superscript:
        run.font.superscript = True


def add_runs(p, text, size=11, bold=False, italic=False, color=None, name=FONT):
    for part in TOKEN.split(text):
        if not part:
            continue
        b, i, t = bold, italic, part
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            b, t = True, part[2:-2]
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            i, t = True, part[1:-1]
        r = p.add_run(t)
        set_font(r, size, b, i, color, name)
    return p


def fmt(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first=0.0, left=0.0, hanging=0.0,
        before=0, after=0, keep_next=False, line=1.0):
    pf = p.paragraph_format
    p.alignment = align
    pf.left_indent = Cm(left + hanging)
    pf.first_line_indent = Cm(first - hanging) if (first or hanging) else Cm(0)
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    if line != 1.0:
        pf.line_spacing = line
    pf.keep_with_next = keep_next
    pf.widow_control = True
    return p


def shade(cell, fill):
    tcpr = cell._element.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcpr.append(shd)


def cell_borders(cell, **edges):
    """edges: top/bottom/left/right = (sz, warna) atau None untuk tanpa garis."""
    tcpr = cell._element.get_or_add_tcPr()
    borders = tcpr.find(qn("w:tcBorders"))
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tcpr.append(borders)
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{edge}")
        spec = edges.get(edge)
        if spec:
            el.set(qn("w:val"), "single")
            el.set(qn("w:sz"), str(spec[0]))
            el.set(qn("w:space"), "0")
            el.set(qn("w:color"), spec[1])
        else:
            el.set(qn("w:val"), "nil")
        borders.append(el)


def cell_margins(cell, top=0, bottom=0, left=60, right=60):
    tcpr = cell._element.get_or_add_tcPr()
    mar = OxmlElement("w:tcMar")
    for k, v in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        el = OxmlElement(f"w:{k}")
        el.set(qn("w:w"), str(v))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tcpr.append(mar)


def set_table_width(table, widths_cm):
    table.autofit = False
    tblpr = table._element.tblPr
    tblw = tblpr.find(qn("w:tblW"))
    if tblw is None:
        tblw = OxmlElement("w:tblW")
        tblpr.append(tblw)
    tblw.set(qn("w:type"), "dxa")
    tblw.set(qn("w:w"), str(int(sum(widths_cm) * 567)))
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblpr.append(layout)
    grid = table._tbl.tblGrid
    for idx, col in enumerate(grid.findall(qn("w:gridCol"))):
        col.set(qn("w:w"), str(int(widths_cm[idx] * 567)))
    for row in table.rows:
        for idx, w in enumerate(widths_cm):
            row.cells[idx].width = Cm(w)


def add_field(p, instr, size=10, bold=True, color="FFFFFF", name=FONT):
    def mk(kind):
        r = p.add_run()
        set_font(r, size, bold, None, color, name)
        fc = OxmlElement("w:fldChar")
        fc.set(qn("w:fldCharType"), kind)
        r._element.append(fc)
        return r

    mk("begin")
    r = p.add_run()
    set_font(r, size, bold, None, color, name)
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = f" {instr} "
    r._element.append(it)
    mk("separate")
    r = p.add_run("1")
    set_font(r, size, bold, None, color, name)
    mk("end")


def set_lang(doc, lang="id-ID"):
    styles = doc.styles.element
    rpr_default = styles.find(qn("w:docDefaults"))
    if rpr_default is not None:
        rpr = rpr_default.find(qn("w:rPrDefault"))
        if rpr is not None:
            r = rpr.find(qn("w:rPr"))
            if r is not None:
                for el in r.findall(qn("w:lang")):
                    r.remove(el)
                lg = OxmlElement("w:lang")
                lg.set(qn("w:val"), lang)
                lg.set(qn("w:eastAsia"), lang)
                lg.set(qn("w:bidi"), "ar-SA")
                r.append(lg)


# ---------------------------------------------------------------- header & footer
def build_header(section, teks):
    section.header.is_linked_to_previous = False
    hdr = section.header
    for p in hdr.paragraphs:
        p._element.getparent().remove(p._element)
    tbl = hdr.add_table(rows=1, cols=2, width=Cm(LEBAR_TEKS_CM))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_width(tbl, [15.2, 1.4])
    c_text, c_num = tbl.rows[0].cells
    rule = (8, "D9D9D9")
    for c in (c_text, c_num):
        cell_borders(c, bottom=rule)
        cell_margins(c, top=20, bottom=40)
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p = c_text.paragraphs[0]
    fmt(p, WD_ALIGN_PARAGRAPH.RIGHT)
    add_runs(p, teks, size=9, bold=True, color="FF0000")
    shade(c_num, "7F7F7F")
    p = c_num.paragraphs[0]
    fmt(p, WD_ALIGN_PARAGRAPH.CENTER)
    add_field(p, "PAGE", size=10, bold=False, color="FFFFFF", name="Times New Roman")
    # paragraf kosong wajib setelah tabel di header
    tail = hdr.add_paragraph()
    fmt(tail, WD_ALIGN_PARAGRAPH.LEFT)
    tail.paragraph_format.line_spacing = Pt(2)
    set_font(tail.add_run(""), 2)


def build_footer(section, teks):
    section.footer.is_linked_to_previous = False
    ftr = section.footer
    for p in ftr.paragraphs:
        p._element.getparent().remove(p._element)
    tbl = ftr.add_table(rows=1, cols=1, width=Cm(LEBAR_TEKS_CM))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_width(tbl, [LEBAR_TEKS_CM])
    c = tbl.rows[0].cells[0]
    shade(c, "404040")
    cell_borders(c, top=(12, "4F81BD"))
    cell_margins(c, top=60, bottom=60)
    c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p = c.paragraphs[0]
    fmt(p, WD_ALIGN_PARAGRAPH.CENTER)
    add_runs(p, teks, size=9, color="FFFFFF", name=FONT_ALT)
    tail = ftr.add_paragraph()
    fmt(tail, WD_ALIGN_PARAGRAPH.LEFT)
    tail.paragraph_format.line_spacing = Pt(2)
    set_font(tail.add_run(""), 2)


# ---------------------------------------------------------------- blok isi
def heading(doc, teks, before=12):
    p = doc.add_paragraph()
    fmt(p, WD_ALIGN_PARAGRAPH.LEFT, before=before, after=3, keep_next=True)
    add_runs(p, teks, size=11, bold=True)
    return p


def subheading(doc, teks):
    p = doc.add_paragraph()
    fmt(p, WD_ALIGN_PARAGRAPH.LEFT, before=11, after=2, keep_next=True)
    add_runs(p, teks, size=11, bold=True)
    return p


def body(doc, teks):
    p = doc.add_paragraph()
    fmt(p, WD_ALIGN_PARAGRAPH.JUSTIFY, first=INDENT_CM)
    add_runs(p, teks, size=11)
    return p


def label_block(doc, label, teks, italic_text=True, hang_cm=2.75, before=11):
    """'Kata Kunci:' / 'Keyword:' dengan indentasi menggantung."""
    p = doc.add_paragraph()
    fmt(p, WD_ALIGN_PARAGRAPH.JUSTIFY, hanging=hang_cm, before=before)
    add_runs(p, label, size=11, bold=True)
    tab = OxmlElement("w:tab")
    r = p.add_run()
    r._element.append(tab)
    set_font(r, 11)
    pPr = p._element.get_or_add_pPr()
    tabs = OxmlElement("w:tabs")
    t = OxmlElement("w:tab")
    t.set(qn("w:val"), "left")
    t.set(qn("w:pos"), str(int(hang_cm * 567)))
    tabs.append(t)
    pPr.append(tabs)
    add_runs(p, teks, size=11, italic=italic_text)
    return p


def spacer(doc, pts=12):
    p = doc.add_paragraph()
    fmt(p, WD_ALIGN_PARAGRAPH.LEFT)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    p.paragraph_format.line_spacing = Pt(pts)
    set_font(p.add_run(""), 2)
    return p


def add_table(doc, nomor, spec):
    cap = doc.add_paragraph()
    fmt(cap, WD_ALIGN_PARAGRAPH.CENTER, before=6, after=3, keep_next=True)
    add_runs(cap, f"Tabel {nomor}. {spec['judul']}", size=10, bold=True)
    header, rows = spec["kepala"], spec["baris"]
    tbl = doc.add_table(rows=1 + len(rows), cols=len(header))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    lebar = spec.get("lebar_cm") or [round(LEBAR_TEKS_CM / len(header), 2)] * len(header)
    set_table_width(tbl, lebar)
    last = len(rows)
    for ri, row in enumerate([header] + rows):
        for ci, val in enumerate(row):
            c = tbl.rows[ri].cells[ci]
            top = (12, "000000") if ri == 0 else None
            bottom = (8, "000000") if ri == 0 else ((12, "000000") if ri == last else None)
            cell_borders(c, top=top, bottom=bottom)
            cell_margins(c, top=30, bottom=30, left=80, right=80)
            p = c.paragraphs[0]
            fmt(p, WD_ALIGN_PARAGRAPH.LEFT)
            add_runs(p, str(val), size=10, bold=(ri == 0))
    spacer(doc, 12)  # spasi baris 12 pt setelah tabel


def add_figure(doc, nomor, spec, base_dir):
    path = spec["berkas"]
    if not os.path.isabs(path):
        path = os.path.join(base_dir, path)
    p = doc.add_paragraph()
    fmt(p, WD_ALIGN_PARAGRAPH.CENTER, before=6, after=3, keep_next=True)
    p.add_run().add_picture(path, width=Cm(spec.get("lebar_cm", 11)))
    cap = doc.add_paragraph()
    fmt(cap, WD_ALIGN_PARAGRAPH.CENTER, after=8)
    add_runs(cap, f"Gambar {nomor}. {spec['judul']}", size=10)


# ---------------------------------------------------------------- program utama
def build(art, out_path, base_dir="."):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(2.2)
    sec.top_margin, sec.bottom_margin = Cm(2.2), Cm(2.0)
    sec.header_distance, sec.footer_distance = Cm(0.7), Cm(0.9)

    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(11)
    rpr = normal.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.insert(0, rf)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rf.set(qn(attr), FONT)
    set_lang(doc)

    build_header(sec, art.get("header", HEADER_DEFAULT))
    build_footer(sec, art.get("footer", FOOTER_DEFAULT))

    # judul
    p = doc.add_paragraph()
    fmt(p, WD_ALIGN_PARAGRAPH.CENTER, before=6, after=10)
    add_runs(p, art["judul"], size=24, bold=True)

    # penulis (1 = nomor afiliasi, amplop = corresponding author)
    p = doc.add_paragraph()
    fmt(p, WD_ALIGN_PARAGRAPH.CENTER, after=0)
    add_runs(p, art["penulis"], size=11, bold=True)
    r = p.add_run("1")
    set_font(r, 11, True, superscript=True)
    r = p.add_run(MARK)
    set_font(r, 11, False, superscript=True)
    p = doc.add_paragraph()
    fmt(p, WD_ALIGN_PARAGRAPH.CENTER, after=10)
    add_runs(p, f"(1) {art['afiliasi']}", size=11)

    p = doc.add_paragraph()
    fmt(p, WD_ALIGN_PARAGRAPH.LEFT, after=0)
    r = p.add_run(MARK + " ")
    set_font(r, 9, name=FONT_ALT)
    add_runs(p, "Corresponding author", size=9, name=FONT_ALT)
    p = doc.add_paragraph()
    fmt(p, WD_ALIGN_PARAGRAPH.LEFT, after=12)
    add_runs(p, f"({art['email']})", size=9, name=FONT_ALT)

    # abstrak Indonesia
    p = doc.add_paragraph()
    fmt(p, WD_ALIGN_PARAGRAPH.CENTER, before=2, after=8, keep_next=True)
    add_runs(p, "Abstrak", size=11, bold=True)
    p = doc.add_paragraph()
    fmt(p, WD_ALIGN_PARAGRAPH.JUSTIFY)
    add_runs(p, art["abstrak"], size=11)
    label_block(doc, "Kata Kunci:", "; ".join(art["kata_kunci"]), italic_text=True, hang_cm=2.75)

    # abstract Inggris
    p = doc.add_paragraph()
    fmt(p, WD_ALIGN_PARAGRAPH.CENTER, before=12, after=8, keep_next=True)
    add_runs(p, "Abstract", size=11, bold=True)
    p = doc.add_paragraph()
    fmt(p, WD_ALIGN_PARAGRAPH.JUSTIFY)
    add_runs(p, art["abstract"], size=11, italic=True)
    label_block(doc, "Keyword:", "; ".join(art["keywords"]), italic_text=True, hang_cm=2.0)

    # pendahuluan
    heading(doc, "PENDAHULUAN", before=16)
    for para in art["pendahuluan"]:
        body(doc, para)

    # pembahasan
    pemb = art["pembahasan"]
    heading(doc, "PEMBAHASAN")
    for para in pemb.get("pengantar", []):
        body(doc, para)
    n_tab = n_gbr = 0
    for sub in pemb["subjudul"]:
        subheading(doc, sub["judul"])
        for para in sub["paragraf"]:
            body(doc, para)
        if sub.get("tabel"):
            n_tab += 1
            add_table(doc, n_tab, sub["tabel"])
        if sub.get("gambar"):
            n_gbr += 1
            add_figure(doc, n_gbr, sub["gambar"], base_dir)

    # simpulan
    heading(doc, "SIMPULAN")
    body(doc, art["simpulan"])

    # ucapan terima kasih (opsional)
    if art.get("ucapan_terima_kasih"):
        heading(doc, "UCAPAN TERIMA KASIH")
        body(doc, art["ucapan_terima_kasih"])

    # daftar pustaka: APA 7th, alfabetis, indentasi menggantung 1 cm
    heading(doc, "DAFTAR PUSTAKA")
    for ref in sorted(art["rujukan"], key=sort_key):
        p = doc.add_paragraph()
        fmt(p, WD_ALIGN_PARAGRAPH.LEFT, hanging=1.0, after=4)
        add_runs(p, format_reference(ref), size=11)

    cp = doc.core_properties
    cp.title = re.sub(r"\*", "", art["judul"])
    cp.author = art["penulis"]
    cp.language = "id-ID"
    doc.save(out_path)
    return out_path


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Pemakaian: python3 build_docx.py article.json keluaran.docx")
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding="utf-8") as f:
        data = json.load(f)
    build(data, dst, base_dir=os.path.dirname(os.path.abspath(src)))
    print(f"OK -> {dst}")
