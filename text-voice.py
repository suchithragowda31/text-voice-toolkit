#!/usr/bin/env python3
"""
text_to_voice.py - Convert text/pdf/txt to WAV using Piper TTS

HOW TO RUN:
  python text-voice.py --text "Hello world"
  python text-voice.py --pdf article.pdf --output article.wav
  python text-voice.py --txt notes.txt --speed 0.75 --output slow.wav

THEN PLAY:
  ffplay output.wav
"""

import argparse, sys, os, subprocess, tempfile

# Path to piper binary
PIPER = os.path.expanduser("~/.local/bin/piper")

# Path to voice model - must be in same folder as this script
MODEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "en_US-lessac-medium.onnx")


def read_pdf(path):
    """Extract all text from a PDF file."""
    from pypdf import PdfReader
    text = "\n\n".join(p.extract_text() or "" for p in PdfReader(path).pages).strip()
    if not text:
        sys.exit("ERROR: Could not read PDF. It may be a scanned image PDF.")
    return text


def read_txt(path):
    """Read a plain text file."""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read().strip()


def speak(text, output_wav, speed):
    """Convert text to WAV using Piper. Optionally change speed with ffmpeg."""

    if not os.path.exists(PIPER):
        sys.exit(f"ERROR: Piper not found at {PIPER}\nRun: pip install piper-tts --break-system-packages")
    if not os.path.exists(MODEL):
        sys.exit(f"ERROR: Model not found: {MODEL}\nMake sure en_US-lessac-medium.onnx is in the same folder as this script.")

    if speed == 1.0:
        # No speed change — pipe text directly into piper and save WAV
        print("  Generating speech with Piper...")
        result = subprocess.run(
            [PIPER, "--model", MODEL, "--output_file", output_wav],
            input=text.encode("utf-8"),
            capture_output=True
        )
        if result.returncode != 0:
            sys.exit(f"Piper failed:\n{result.stderr.decode()}")

    else:
        # Speed change needed — generate to temp WAV, then use ffmpeg atempo filter
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            wav_tmp = tmp.name
        try:
            print("  Generating speech with Piper...")
            result = subprocess.run(
                [PIPER, "--model", MODEL, "--output_file", wav_tmp],
                input=text.encode("utf-8"),
                capture_output=True
            )
            if result.returncode != 0:
                sys.exit(f"Piper failed:\n{result.stderr.decode()}")

            # atempo filter only accepts 0.5-2.0, so chain multiple filters for other speeds
            def speed_filter(s):
                filters = []
                while s < 0.5:
                    filters.append("atempo=0.5")
                    s /= 0.5
                while s > 2.0:
                    filters.append("atempo=2.0")
                    s /= 2.0
                filters.append(f"atempo={s:.4f}")
                return ",".join(filters)

            print(f"  Applying speed {speed}x with ffmpeg...")
            result = subprocess.run(
                ["ffmpeg", "-y", "-i", wav_tmp, "-filter:a", speed_filter(speed), output_wav],
                capture_output=True
            )
            if result.returncode != 0:
                sys.exit(f"ffmpeg failed:\n{result.stderr.decode()}")
        finally:
            if os.path.exists(wav_tmp):
                os.remove(wav_tmp)


def main():
    parser = argparse.ArgumentParser(description="Convert text/pdf/txt to WAV using Piper TTS")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--text", metavar="TEXT", help='Text in quotes e.g. --text "hello world"')
    group.add_argument("--pdf",  metavar="PATH", help="PDF file e.g. --pdf article.pdf")
    group.add_argument("--txt",  metavar="PATH", help="Text file e.g. --txt notes.txt")

    parser.add_argument("--output", default="output.wav", help="Output filename (default: output.wav)")
    parser.add_argument("--speed",  type=float, default=1.0, help="Speed: 0.5=slow 1.0=normal 1.5=fast")

    args = parser.parse_args()

    if not any([args.text, args.pdf, args.txt]):
        parser.print_help()
        print('\nExamples:')
        print('  python text-voice.py --text "Hello world"')
        print('  python text-voice.py --pdf article.pdf --output article.wav')
        print('  python text-voice.py --txt notes.txt --speed 0.75 --output slow.wav')
        sys.exit(1)

    print("\n📄 Reading input...")
    if args.pdf:
        text = read_pdf(args.pdf)
        print(f"  Extracted {len(text):,} characters from {args.pdf}")
    elif args.txt:
        text = read_txt(args.txt)
        print(f"  Loaded {len(text):,} characters from {args.txt}")
    else:
        text = args.text
        print(f"  Got {len(text):,} characters")

    output = args.output if args.output.endswith(".wav") else args.output + ".wav"

    print(f"\n🎙️  Converting to speech...")
    speak(text, output, args.speed)

    size_mb = os.path.getsize(output) / (1024 * 1024)
    print(f"\n✅ Done!")
    print(f"   File : {output} ({size_mb:.1f} MB)")
    print(f"   Play : ffplay {output}\n")


if __name__ == "__main__":
    main()