#!/usr/bin/env python3
"""
speech_to_text.py - Convert audio (WAV/MP3) to text using Whisper
------------------------------------------------------------------
HOW TO RUN:
  python speech-to-text.py --audio recording.wav
  python speech-to-text.py --audio meeting.mp3
  python speech-to-text.py --audio lecture.wav --output transcript.txt

THEN READ:
  cat transcript.txt

FIRST TIME SETUP:
  pip install openai-whisper --break-system-packages
  sudo apt install ffmpeg   (already installed)
"""

import argparse, sys, os

def transcribe(audio_path, output_txt, model_size):
    """
    Load Whisper model and transcribe the audio file to text.
    Model sizes: tiny, base, small, medium, large
    - tiny/base = fast but less accurate
    - small/medium = good balance (recommended)
    - large = most accurate but slow
    First run downloads the model automatically.
    """
    try:
        import whisper
    except ImportError:
        sys.exit("Whisper not installed.\nRun: pip install openai-whisper --break-system-packages")

    if not os.path.exists(audio_path):
        sys.exit(f"ERROR: Audio file not found: {audio_path}")

    print(f"  Loading Whisper model ({model_size})...")
    print("  (First time will download the model - please wait)")
    model = whisper.load_model(model_size)

    print(f"  Transcribing {audio_path}...")
    result = model.transcribe(audio_path)
    text = result["text"].strip()

    # Save to output file
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(text)

    return text


def main():
    parser = argparse.ArgumentParser(description="Convert audio to text using Whisper")
    parser.add_argument("--audio",  metavar="PATH", required=True, help="Audio file e.g. --audio recording.wav")
    parser.add_argument("--output", metavar="PATH", default="transcript.txt", help="Output text file (default: transcript.txt)")
    parser.add_argument("--model",  default="small", choices=["tiny","base","small","medium","large"],
                        help="Whisper model size (default: small). Larger = more accurate but slower.")

    args = parser.parse_args()

    output = args.output if args.output.endswith(".txt") else args.output + ".txt"

    print(f"\n🎙️  Reading audio: {args.audio}")
    text = transcribe(args.audio, output, args.model)

    print(f"\n✅ Done!")
    print(f"   File    : {output}")
    print(f"   Preview : {text[:200]}...")
    print(f"\n   Read full transcript: cat {output}\n")


if __name__ == "__main__":
    main()