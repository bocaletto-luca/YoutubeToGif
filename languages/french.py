#!/usr/bin/env python3
"""
youtube2gif.py

Télécharger une vidéo YouTube et la convertir en GIF en n'utilisant que yt-dlp et ffmpeg.
Dépendances système (installez-les si vous ne les avez pas) :
    sudo apt install yt-dlp ffmpeg

Utilisation :
    python3 youtube2gif.py URL [start_sec] [duration_sec] [output.gif]

Exemple :
    python3 youtube2gif.py https://youtu.be/kX8hfK0PrHM 10 5 clip.gif
"""

import sys
import os
import subprocess
import tempfile
import shutil

def die(msg, code=1):
    print("ERREUR :", msg, file=sys.stderr)
    sys.exit(code)

def which(cmd):
    path = shutil.which(cmd)
    if not path:
        die(f"'{cmd}' introuvable. Installez avec : sudo apt install {cmd}")
    return path

def run(cmd, **kw):
    print("> " + " ".join(cmd))
    res = subprocess.run(cmd, **kw)
    if res.returncode != 0:
        die(f"commande échouée : {' '.join(cmd)} (rc={res.returncode})")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    url      = sys.argv[1]
    start    = sys.argv[2] if len(sys.argv) > 2 else "0"
    duration = sys.argv[3] if len(sys.argv) > 3 else "5"
    outgif   = sys.argv[4] if len(sys.argv) > 4 else "out.gif"

    yt     = which("yt-dlp")
    ffmpeg = which("ffmpeg")

    tmpdir = tempfile.mkdtemp(prefix="yt2gif_")
    try:
        mp4 = os.path.join(tmpdir, "video.mp4")
        pal = os.path.join(tmpdir, "palette.png")

        # 1) Télécharger et fusionner la meilleure vidéo + audio
        run([yt,
             "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
             "--merge-output-format", "mp4",
             "-o", mp4,
             url])

        # 2) Générer la palette
        run([ffmpeg,
             "-v", "warning",
             "-ss", start,
             "-t", duration,
             "-i", mp4,
             "-vf", "fps=10,scale=320:-1:flags=lanczos,palettegen",
             "-y", pal])

        # 3) Créer le GIF
        run([ffmpeg,
             "-v", "warning",
             "-ss", start,
             "-t", duration,
             "-i", mp4,
             "-i", pal,
             "-filter_complex", "fps=10,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse",
             "-y", outgif])

        print(f"\n✔ GIF enregistré sous : {outgif}")

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

if __name__ == "__main__":
    main()

