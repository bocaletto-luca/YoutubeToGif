#!/usr/bin/env bash
#
# youtube2gif_full.sh
# Download a full YouTube video and convert it to an animated GIF.
#
# Requirements:
#   • yt-dlp
#   • ffmpeg
#
set -euo pipefail

# CONFIGURATION
URL="https://www.youtube.com/watch?v=kX8hfK0PrHM"
FPS=12                   # frames per second for the GIF
WIDTH=320                # GIF width in pixels (height auto)
OUTPUT="full_video.gif"

# TEMP DIRECTORY (auto-cleaned)
TMPDIR="$(mktemp -d)"
TMP_VIDEO="$TMPDIR/video.mp4"
PALETTE="$TMPDIR/palette.png"

cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

# 1) Download & merge best video+audio
echo "Downloading and merging best formats..."
yt-dlp \
  -f bestvideo+bestaudio \
  --merge-output-format mp4 \
  -o "$TMP_VIDEO" \
  "$URL"

# 2) Generate palette for best colors
echo "Generating palette..."
ffmpeg -v warning \
  -i "$TMP_VIDEO" \
  -vf "fps=${FPS},scale=${WIDTH}:-1:flags=lanczos,palettegen" \
  -y "$PALETTE"

# 3) Create the final GIF
echo "Creating GIF..."
ffmpeg -v warning \
  -i "$TMP_VIDEO" \
  -i "$PALETTE" \
  -filter_complex "fps=${FPS},scale=${WIDTH}:-1:flags=lanczos[x];[x][1:v]paletteuse" \
  -y "$OUTPUT"

echo "✔ Done! GIF saved to ${OUTPUT}"
