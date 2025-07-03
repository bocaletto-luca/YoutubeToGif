# pip install pytube moviepy

import os, tempfile, argparse
from pytube import YouTube
from moviepy.editor import VideoFileClip

def yt_to_gif(url, start, duration, out):
    # 1) download
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4')\
                     .order_by('resolution').desc().first()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
    stream.download(filename=tmp)

    # 2) trim & convert
    clip = VideoFileClip(tmp).subclip(start, start + duration)
    clip.write_gif(out, fps=12, program='ffmpeg')
    clip.close()

    # 3) cleanup
    os.remove(tmp)

if __name__ == '__main__':
    p = argparse.ArgumentParser(description="YouTube→GIF converter")
    p.add_argument('url', help="YouTube video URL")
    p.add_argument('-s','--start', type=float, default=0, help="start time (sec)")
    p.add_argument('-d','--duration', type=float, default=5, help="duration (sec)")
    p.add_argument('-o','--output', default='out.gif', help="output GIF file")
    args = p.parse_args()
    yt_to_gif(args.url, args.start, args.duration, args.output)
