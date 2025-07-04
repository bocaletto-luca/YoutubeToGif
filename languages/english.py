#!/usr/bin/env python3
"""
youtube2gif.py

Download a YouTube video and convert it into a GIF using only yt-dlp and ffmpeg.
System dependencies (install if you don't have them):
    sudo apt install yt-dlp ffmpeg

Usage:
    python3 youtube2gif.py URL [start_sec] [duration_sec] [output.gif]

Example:
    python3 youtube2gif.py https://youtu.be/kX8hfK0PrHM 10 5 clip.gif
"""

import sys
import os
import subprocess
import tempfile
import shutil

def die(msg, code=1):
    print("ERROR:", msg, file=sys.stderr)
    sys.exit(code)

def which(cmd):
    path = shutil.which(cmd)
    if not path:
        die(f"'{cmd}' not found. Install with: sudo apt install {cmd}")
    return path

def run(cmd, **kw):
    print("> " + " ".join(cmd))
    res = subprocess.run(cmd, **kw)
    if res.returncode != 0:
        die(f"command failed: {' '.join(cmd)} (rc={res.returncode})")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    url      = sys.argv[1]
    start    = sys.argv[2] if len(sys.argv) > 2 else "0"
    duration = sys.argv[3] if len(sys.argv) > 3 else "5"
    outgif   = sys.argv[4] if len(sys.argv) > 4 else "out.gif"

    yt       = which("yt-dlp")
    ffmpeg   = which("ffmpeg")

    tmpdir = tempfile.mkdtemp(prefix="yt2gif_")
    try:
        mp4 = os.path.join(tmpdir, "video.mp4")
        pal = os.path.join(tmpdir, "palette.png")

        # 1) Download and merge best video+audio
        run([yt,
             "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
             "--merge-output-format", "mp4",
             "-o", mp4,
             url])

        # 2) Generate palette
        run([ffmpeg,
             "-v", "warning",
             "-ss", start,
             "-t", duration,
             "-i", mp4,
             "-vf", "fps=10,scale=320:-1:flags=lanczos,palettegen",
             "-y", pal])

        # 3) Create the GIF
        run([ffmpeg,
             "-v", "warning",
             "-ss", start,
             "-t", duration,
             "-i", mp4,
             "-i", pal,
             "-filter_complex", "fps=10,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse",
             "-y", outgif])

        print(f"\n✔ GIF saved to: {outgif}")

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

if __name__ == "__main__":
    main()
