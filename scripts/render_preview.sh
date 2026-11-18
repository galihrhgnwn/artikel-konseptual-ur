#!/usr/bin/env bash
# Render .docx -> PDF -> PNG untuk pemeriksaan visual (header, footer, judul, halaman).
# Pemakaian: bash render_preview.sh artikel.docx [folder_keluaran]
# Lato bawaan skill (assets/fonts) dipasang otomatis; Carlito hanya cadangan terakhir.
set -euo pipefail
DOCX="${1:?Pemakaian: render_preview.sh artikel.docx [folder_keluaran]}"
OUT="${2:-$(dirname "$DOCX")/pratinjau}"
mkdir -p "$OUT"

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if ! [ -n "$(fc-list 2>/dev/null | grep -i lato || true)" ]; then
  bash "$HERE/install_fonts.sh" || true
fi
if ! [ -n "$(fc-list 2>/dev/null | grep -i lato || true)" ]; then
  # cadangan terakhir: Carlito (turunan Lato)
  CONF="$(mktemp -d)"
  cat > "$CONF/fonts.conf" <<'EOF2'
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <include ignore_missing="yes">/etc/fonts/fonts.conf</include>
  <alias binding="same"><family>Lato</family><prefer><family>Carlito</family></prefer></alias>
</fontconfig>
EOF2
  export FONTCONFIG_FILE="$CONF/fonts.conf"
  echo "Catatan: Lato gagal terpasang; pratinjau memakai Carlito."
fi

soffice --headless --convert-to pdf --outdir "$OUT" "$DOCX" >/dev/null 2>&1
PDF="$OUT/$(basename "${DOCX%.docx}").pdf"
pdftoppm -r 80 -png "$PDF" "$OUT/halaman"
echo "Halaman: $(pdfinfo "$PDF" | awk '/Pages/{print $2}')"
echo "PDF   : $PDF"
ls "$OUT"/halaman*.png
