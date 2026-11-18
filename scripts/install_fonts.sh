#!/usr/bin/env bash
# Pasang Lato bawaan skill (assets/fonts) untuk pengguna saat ini, tanpa internet dan tanpa hak root.
# Pemakaian: bash install_fonts.sh
set -euo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/../assets/fonts" && pwd)"
DST="${HOME}/.local/share/fonts/lato-artikel"
mkdir -p "$DST"
cp "$SRC"/Lato-*.ttf "$SRC"/OFL.txt "$DST"/
command -v fc-cache >/dev/null && fc-cache -f "$DST" >/dev/null 2>&1 || true
if command -v fc-list >/dev/null && [ -n "$(fc-list 2>/dev/null | grep -i lato || true)" ]; then
  echo "Lato terpasang: $(fc-list | grep -i lato | wc -l) gaya."
else
  echo "Salin selesai ke $DST, tetapi fc-list belum melihat Lato; lanjutkan, pratinjau akan memakai fontconfig sendiri." >&2
fi
