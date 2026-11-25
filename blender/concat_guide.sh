#!/usr/bin/env bash
# Skleja paczki prowadnicy z 3D Jutsu w jeden plik 24 fps, 9:16, gotowy jako wejscie do Seedance video_edit.
# Uzycie: concat_guide.sh <katalog_z_paczkami> <plik_wyjsciowy.mp4>
set -euo pipefail
DIR="$1"; OUT="$2"
LIST="$(mktemp)"
for f in $(ls "$DIR"/g[0-9][0-9][0-9].mp4 | sort); do echo "file '$f'" >> "$LIST"; done
# Seedance video_edit wymaga min. 720p -> skalowanie 432x768 do 720x1280 (lanczos), bez dzwieku
ffmpeg -v error -f concat -safe 0 -i "$LIST" \
  -vf "scale=720:1280:flags=lanczos,fps=24,format=yuv420p" \
  -c:v libx264 -crf 14 -preset slow -an -movflags +faststart "$OUT" -y
ffprobe -v error -show_entries stream=width,height,nb_frames,r_frame_rate -show_entries format=duration -of compact "$OUT"
