# Youtube ToGif
#### Author: Bocaletto Luca

youtube2gif.py is a lightweight Python script that leverages system-installed yt-dlp and FFmpeg to download YouTube videos (or specific segments) and convert them into high-quality animated GIFs. It supports full-length or custom slices with configurable FPS and width, generates optimized palettes for vibrant colors, and automatically cleans up temporary files.

---

## Example GIF Create

<div align="center">
  [![GIF Preview di Luca Bocaletto](luca-bocaletto.gif)](https://www.youtube.com/watch?v=kX8hfK0PrHM)
</div>

---

## Table of Contents

- [Features](#features)  
- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [Usage](#usage)  
  - [Full-length GIF](#full-length-gif)  
  - [Custom slice GIF](#custom-slice-gif)  
  - [All options](#all-options)  
- [How It Works](#how-it-works)  
- [Repository Structure](#repository-structure)  
- [Author](#author)  
- [License](#license)  

---

## Features

- Download any public YouTube video in the best available quality  
- Two-pass color palette generation for optimal GIF colors  
- Support for full-length conversion or custom start/duration slices  
- Configurable FPS and output width  
- No Python libraries required beyond the standard library—relies on `yt-dlp` and `ffmpeg`  

---

## Prerequisites

- **Python 3.6+** (the script uses only the standard library)  
- **yt-dlp** (YouTube downloader)  
- **ffmpeg** (video processing and GIF creation)  

On Debian/Ubuntu:

```bash
sudo apt update
sudo apt install yt-dlp ffmpeg python3
```

Ensure both `yt-dlp` and `ffmpeg` are available on your `PATH`:

```bash
which yt-dlp
which ffmpeg
```

---

## Installation

1. Clone this repository (or download `youtube2gif.py` directly):

   ```bash
   git clone https://github.com/bocaletto-luca/YoutubeToGif.git
   cd YoutubeToGif
   ```

2. Make the script executable:

   ```bash
   chmod +x youtube2gif.py
   ```

3. You’re ready to run it—no further installation required.

---

## Usage

```bash
./youtube2gif.py URL [--start START_SEC] [--duration DURATION_SEC] [--full] [--output FILE] [--fps N] [--width PX]
```

### Full-length GIF

Convert the entire video (start at 0, run to end):

```bash
./youtube2gif.py "https://www.youtube.com/watch?v=kX8hfK0PrHM" --full --output full.gif
```

### Custom slice GIF

Convert a specific segment:

```bash
./youtube2gif.py "https://youtu.be/kX8hfK0PrHM" \
  --start 10 \
  --duration 5 \
  --output clip.gif
```

### All options

```text
  Positional argument:
    url                   YouTube video URL

  Optional arguments:
    --start START_SEC     Start time in seconds (default: 0.0)
    --duration DURATION   Duration in seconds (default: None if --full)
    --full                Convert the full video (overrides --duration)
    --output FILE         Output GIF filename (default: out.gif)
    --fps N               Frames per second for GIF (default: 10)
    --width PX            Maximum width of GIF in pixels (default: 320)
    -h, --help            Show this help message and exit
```

---

## How It Works

1. **Download**  
   Uses `yt-dlp` to fetch the best MP4 video + audio, merging them into a single temporary file.  

2. **Palette Generation**  
   Runs `ffmpeg` with `palettegen` filter for two-pass color optimization.  

3. **GIF Creation**  
   Runs `ffmpeg` again with `paletteuse` filter to create a smooth, colorful GIF at the chosen FPS and width.  

4. **Cleanup**  
   Deletes all temporary files when finished.

---

## Repository Structure

```
YoutubeToGif/
├── README.md
└── youtube2gif.py
```

- **README.md**: This documentation.  
- **youtube2gif.py**: The executable Python script.

---

## Author

**@bocaletto-luca**  
GitHub: [https://github.com/bocaletto-luca](https://github.com/bocaletto-luca)  

---

## License

This project is released under the **GPL-3.0 License**. See [LICENSE](LICENSE) for details.
