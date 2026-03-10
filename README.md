# Text ↔ Voice Toolkit

Free, offline, open-source audio toolkit in Python. No subscriptions, no internet needed after setup.


## 📄 → 🔊 Text to Voice
Convert any PDF, TXT file, or plain text to audio using Piper TTS.

Install:

pip install piper-tts pypdf pydub --break-system-packages
sudo apt install ffmpeg espeak espeak-ng


Download voice model:

wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json


Run:

python text-voice.py --text "Hello world"
python text-voice.py --pdf article.pdf --output article.wav
python text-voice.py --txt notes.txt --speed 0.75 --output slow.wav



## 🔊 → 📄 Speech to Text
Transcribe any audio file to text using OpenAI Whisper.

Install:

pip install openai-whisper --break-system-packages


Run:

python speech-to-text.py --audio recording.wav
python speech-to-text.py --audio meeting.mp3 --output notes.txt




## Tools Used
- [Piper TTS](https://github.com/rhasspy/piper) - Text to speech
- [OpenAI Whisper](https://github.com/openai/whisper) - Speech to text
- [pypdf](https://github.com/py-pdf/pypdf) - PDF text extraction
- [ffmpeg](https://ffmpeg.org) - Audio processing