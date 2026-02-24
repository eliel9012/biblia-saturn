#!/bin/bash
set -euo pipefail

NCPU="$(nproc)"

# Sync UI + book artwork into the CD tree (short uppercase names).
python3 ../tools/sync_cd_images.py --src-dir ../Saturn_Biblia_Images/tga_format --out-dir ./cd

# Generate small UI textures used as VDP1 sprites (cards).
python3 ../tools/gen_ui_cards.py --out-dir ./cd/UI

# (Re)generate the font from a bitmap ISO-8859-1 source (includes baked shadow).
python3 ../tools/gen_font_tga_template.py \
  --out-tga ./cd/FONT.TGA \
  --out-header ./font_mapping.h \
  --preview-png ./FONT_PREVIEW.png \
  --shadow drop

# (Re)generate Bible data assets used by the prototype.
python3 ../tools/gen_bible_assets.py --json ../acf_clean.json --out-dir ./cd

make clean
make -j"${NCPU}" all
