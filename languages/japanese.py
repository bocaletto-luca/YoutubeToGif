#!/usr/bin/env python3
# Japanese

"""
youtube2gif.py

YouTubeの動画をダウンロードし、yt-dlpとffmpegのみを使用してGIFに変換します。
システム依存関係（インストールされていない場合は実行）：
    sudo apt install yt-dlp ffmpeg

使用法：
    python3 youtube2gif.py URL [start_sec] [duration_sec] [output.gif]

例：
    python3 youtube2gif.py https://youtu.be/kX8hfK0PrHM 10 5 clip.gif
"""

import sys
import os
import subprocess
import tempfile
import shutil

def die(msg, code=1):
    print("エラー：", msg, file=sys.stderr)
    sys.exit(code)

def which(cmd):
    path = shutil.which(cmd)
    if not path:
        die(f"コマンド '{cmd}' が見つかりません。次を実行してインストールしてください：sudo apt install {cmd}")
    return path

def run(cmd, **kw):
    print("> " + " ".join(cmd))
    res = subprocess.run(cmd, **kw)
    if res.returncode != 0:
        die(f"コマンド失敗：{' '.join(cmd)} (終了コード={res.returncode})")

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

        # 1) ベストな動画と音声をダウンロードおよび結合
        run([yt,
             "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
             "--merge-output-format", "mp4",
             "-o", mp4,
             url])

        # 2) カラーパレットを生成
        run([ffmpeg,
             "-v", "warning",
             "-ss", start,
             "-t", duration,
             "-i", mp4,
             "-vf", "fps=10,scale=320:-1:flags=lanczos,palettegen",
             "-y", pal])

        # 3) GIFを作成
        run([ffmpeg,
             "-v", "warning",
             "-ss", start,
             "-t", duration,
             "-i", mp4,
             "-i", pal,
             "-filter_complex", "fps=10,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse",
             "-y", outgif])

        print(f"\n✔ GIFを保存しました：{outgif}")

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

if __name__ == "__main__":
    main()
