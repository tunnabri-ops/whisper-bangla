#!/usr/bin/env python3
"""Transcribe audio to Bangla text + SRT subtitles with OpenAI Whisper.

Usage:
    python3 transcribe-bangla.py audio.mp3 --model base
    python3 transcribe-bangla.py audio.mp3 --model small --output-dir out/

Outputs (next to the input file, or in --output-dir):
    <name>.txt  - full Bangla transcript
    <name>.srt  - subtitles with timestamps

Requires: pip install -r requirements.txt  (openai-whisper)
System dependency: ffmpeg (see upstream README:
https://github.com/openai/whisper)
"""

import argparse
import os
import sys


def format_timestamp(seconds: float) -> str:
    """Format seconds as SRT timestamp HH:MM:SS,mmm."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def write_srt(segments, path: str) -> None:
    """Write Whisper segments as an SRT subtitle file."""
    with open(path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, start=1):
            start = format_timestamp(float(seg["start"]))
            end = format_timestamp(float(seg["end"]))
            text = seg["text"].strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Transcribe audio to Bangla text + SRT subtitles."
    )
    parser.add_argument("audio", help="Audio file (mp3, wav, flac, m4a, ...)")
    parser.add_argument(
        "--model",
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: base; small = more accurate)",
    )
    parser.add_argument(
        "--language",
        default="bn",
        help="Language code (default: bn for Bangla)",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output folder (default: same folder as the audio file)",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.audio):
        print(f"Error: file not found: {args.audio}", file=sys.stderr)
        return 1

    try:
        import whisper
    except ImportError:
        print(
            "Error: openai-whisper is not installed.\n"
            "Run: pip install -r requirements.txt",
            file=sys.stderr,
        )
        return 1

    out_dir = args.output_dir or os.path.dirname(os.path.abspath(args.audio))
    os.makedirs(out_dir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(args.audio))[0]
    txt_path = os.path.join(out_dir, stem + ".txt")
    srt_path = os.path.join(out_dir, stem + ".srt")

    print(f"Loading model '{args.model}' ...")
    model = whisper.load_model(args.model)

    print(f"Transcribing {args.audio} (language={args.language}) ...")
    result = model.transcribe(args.audio, language=args.language)

    text = result["text"].strip()
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    write_srt(result["segments"], srt_path)

    print(f"Done. Wrote:\n  {txt_path}\n  {srt_path}")
    print(f"Preview: {text[:200]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
