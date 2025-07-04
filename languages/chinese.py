#!/usr/bin/env python3
# Chinese

"""
youtube2gif.py

下载 YouTube 视频并使用 yt-dlp 和 ffmpeg 将其转换为 GIF。
系统依赖（如果没有请安装）：
    sudo apt install yt-dlp ffmpeg

用法：
    python3 youtube2gif.py URL [start_sec] [duration_sec] [output.gif]

示例：
    python3 youtube2gif.py https://youtu.be/kX8hfK0PrHM 10 5 clip.gif
"""

import sys
import os
import subprocess
import tempfile
import shutil

def die(msg, code=1):
    print("错误：", msg, file=sys.stderr)
    sys.exit(code)

def which(cmd):
    path = shutil.which(cmd)
    if not path:
        die(f"未找到 '{cmd}'。请安装：sudo apt install {cmd}")
    return path

def run(cmd, **kw):
    print("> " + " ".join(cmd))
    res = subprocess.run(cmd, **kw)
    if res.returncode != 0:
        die(f"命令失败：{' '.join(cmd)} (返回码 {res.returncode})")

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

        # 1) 下载并合并最佳视频和音频
        run([yt,
             "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
             "--merge-output-format", "mp4",
             "-o", mp4,
             url])

        # 2) 生成调色板
        run([ffmpeg,
             "-v", "warning",
             "-ss", start,
             "-t", duration,
             "-i", mp4,
             "-vf", "fps=10,scale=320:-1:flags=lanczos,palettegen",
             "-y", pal])

        # 3) 创建 GIF
        run([ffmpeg,
             "-v", "warning",
             "-ss", start,
             "-t", duration,
             "-i", mp4,
             "-i", pal,
             "-filter_complex", "fps=10,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse",
             "-y", outgif])

        print(f"\n✔ GIF 已保存至：{outgif}")

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

if __name__ == "__main__":
    main()
