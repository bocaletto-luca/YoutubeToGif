#!/usr/bin/env bash
#
# you2gif.sh
# Download a full YouTube video and convert it to an animated GIF
# with a fallback for format selection.
#
# Requirements:
#   • yt-dlp
#   • ffmpeg
#
set -euo pipefail

URL="https://www.youtube.com/watch?v=kX8hfK0PrHM"
FPS=12
WIDTH=320
OUTPUT="full_video.gif"

TMPDIR="$(mktemp -d)"
TMP_VIDEO="$TMPDIR/video.mp4"
PALETTE="$TMPDIR/palette.png"

cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT

echo "Downloading and merging best available MP4..."
yt-dlp \
  -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo[ext=mp4]/best" \
  --merge-output-format mp4 \
  -o "$TMP_VIDEO" \
  "$URL"

echo "Generating palette..."
ffmpeg -v warning \
  -i "$TMP_VIDEO" \
  -vf "fps=${FPS},scale=${WIDTH}:-1:flags=lanczos,palettegen" \
  -y "$PALETTE"

echo "Creating GIF..."
ffmpeg -v warning \
  -i "$TMP_VIDEO" \
  -i "$PALETTE" \
  -filter_complex "fps=${FPS},scale=${WIDTH}:-1:flags=lanczos[x];[x][1:v]paletteuse" \
  -y "$OUTPUT"

echo "✔ Done! GIF saved to ${OUTPUT}"
