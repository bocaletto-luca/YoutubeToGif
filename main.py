#!/usr/bin/env python3
"""
main.py

Universal entry point for the YoutubeToGif project.
Dispatches your request to the chosen language‐specific script
inside the languages/ folder.

Usage:
    ./main.py [--lang LANG] URL [start_sec] [duration_sec] [output.gif]

Examples:
    # default (English)
    ./main.py https://youtu.be/kX8hfK0PrHM 10 5 clip.gif

    # Italian
    ./main.py --lang italian https://youtu.be/kX8hfK0PrHM 10 5 clip.gif
"""

import os
import sys
import subprocess
import argparse

# directory containing all translations
LANGUAGE_DIR = os.path.join(os.path.dirname(__file__), "languages")

# supported language codes (must match filenames in languages/)
SUPPORTED_LANGS = [
    "english",
    "italian",
    "french",
    "german",
    "spanish",
    "portuguese",
    "russian",
    "chinese",
    "japanese",
]

def list_languages():
    """Print a comma-separated list of available languages."""
    return ", ".join(SUPPORTED_LANGS)

def locate_script(lang):
    """
    Return the full path to the <lang>.py script.
    Exit with error if missing.
    """
    path = os.path.join(LANGUAGE_DIR, f"{lang}.py")
    if not os.path.isfile(path):
        sys.stderr.write(
            f"Error: language script not found: {path}\n"
            f"Available: {list_languages()}\n"
        )
        sys.exit(1)
    return path

def build_command(script, url, start, duration, output):
    """
    Construct the subprocess command:
      [python_executable, script, url, start, duration, output]
    """
    return [
        sys.executable,
        script,
        url,
        start,
        duration,
        output
    ]

def main():
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="YoutubeToGif multilingual launcher"
    )
    parser.add_argument(
        "--lang", "-l",
        choices=SUPPORTED_LANGS,
        default="english",
        help="Language of the script (default: english)"
    )
    parser.add_argument(
        "url",
        help="YouTube video URL"
    )
    parser.add_argument(
        "start",
        nargs="?",
        default="0",
        help="Start time in seconds (default: 0)"
    )
    parser.add_argument(
        "duration",
        nargs="?",
        default="5",
        help="Duration in seconds (default: 5)"
    )
    parser.add_argument(
        "output",
        nargs="?",
        default="out.gif",
        help="Output GIF filename (default: out.gif)"
    )

    args = parser.parse_args()

    # find and validate the language script
    script_path = locate_script(args.lang)

    # prepare the command line
    cmd = build_command(
        script=script_path,
        url=args.url,
        start=args.start,
        duration=args.duration,
        output=args.output
    )

    # run the chosen script and bubble up its exit code
    try:
        exit_code = subprocess.call(cmd)
        sys.exit(exit_code)
    except OSError as e:
        sys.stderr.write(f"Failed to execute {script_path}: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
