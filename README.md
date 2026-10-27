# Steganography Tools

A small, interactive Python command-line project demonstrating how text can be embedded in image, text, WAV audio, and video cover files. It includes sample cover files and a menu-driven interface in `Steganography.py`.

> **Status:** Educational prototype. The implementations have known limitations and are not suitable for protecting sensitive information or for reliable production use. In particular, the video path uses RC4 (obsolete and insecure) and lossy video encoding, which can destroy embedded bits. See [Limitations](#limitations).

## Features

- **Image:** embeds UTF-8 text bits into the least significant bits of RGB pixels; the menu uses `Sample_cover_files/cover_image.jpg` as the encoding cover.
- **Text:** hides encoded bits using zero-width Unicode characters in words from `Sample_cover_files/cover_text.txt`.
- **Audio:** embeds text in WAV frame bytes using a modified least-significant-bit scheme.
- **Video:** experimental single-frame embedding and extraction, with a user-provided key for the RC4 demonstration.

The image, text, and audio paths use a `*^*^*` end marker. Video uses the same marker after encrypting its message.

## Requirements

- Python 3.8 or later
- NumPy
- OpenCV for Python (`opencv-python`)
- For video support, an OpenCV build with a working video codec backend (the example writer requests XVID)

## Setup

From the repository root, create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
```

Run the interactive menu from the repository root so the relative sample-file paths resolve:

```bash
python Steganography.py
```

Choose an operation from the menu and follow the prompts. Image encoding reads the bundled cover image; text encoding reads the bundled cover text; audio encoding asks for a WAV path. The current video implementation reads the bundled cover video and writes `stego_video.mp4` in the current directory.

## Output and decoding

Provide output filenames with the desired extension when prompted. To decode, choose the matching media type and enter the stego file path when requested. Keep the original file format and avoid editing or recompressing the stego file before decoding: even small changes can corrupt the hidden data.

For video, encoding and decoding are intended to happen in the same run of the video submenu; the implementation depends on in-memory frame state. Video handling is experimental and may fail depending on codec support.

## Limitations

- This is a demonstration, not encryption or secure communication. LSB and zero-width-character hiding provide no confidentiality or integrity.
- The video feature uses RC4, which is cryptographically broken and must not be used for security. Its lossy output codec can alter the embedded frame data.
- The command-line program assumes it is launched from the repository root and uses fixed sample paths for text, image, and video encoding.
- Capacity checks, malformed input handling, Unicode support, and media/codec compatibility are limited. Use short, non-sensitive messages and copies of files.
- The code is an interactive prototype; decoding results are printed to the terminal rather than returned as files.

## Project files

```text
Steganography.py                 Interactive implementation
requirements.txt                 Python dependencies
Sample_cover_files/              Example image, text, audio, and video covers
Explanation and Written description/
                                 Supporting presentation and written report
```

