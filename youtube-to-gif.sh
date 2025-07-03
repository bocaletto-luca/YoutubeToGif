# 1. Download best‐quality MP4 to temp file
youtube-dl -f best -o temp.mp4 "https://youtu.be/VIDEO_ID"

# 2. Convert a slice (e.g. from 00:00:10 for 5 seconds) to GIF
ffmpeg -ss 00:00:10 -t 5 -i temp.mp4 \
  -vf "fps=12,scale=320:-1:flags=lanczos" \
  -gifflags -transdiff \
  output.gif

# 3. Clean up
rm temp.mp4
