# Steganography Tools

A small, interactive Python command-line project demonstrating how text can be embedded in image, text, WAV audio, and video cover files. It includes sample cover files and a menu-driven interface in `Steganography.py`.

> **Status:** Educational prototype. The implementations have known limitations and are not suitable for protecting sensitive information or for reliable production use. In particular, the video path uses RC4 (obsolete and insecure) and lossy video encoding, which can destroy embedded bits. See [Limitations](#limitations).

## Features

- **Image:** uses Bit-Plane Complexity Segmentation (BPCS). It divides channel bit-planes into 8×8 blocks, checkerboard-transforms the payload blocks, and embeds them in the cover image. The menu uses `Sample_cover_files/cover_image.jpg` as the encoding cover.
- **Text:** hides encoded bits using zero-width Unicode characters in words from `Sample_cover_files/cover_text.txt`.
- **Audio:** embeds text in WAV frame bytes using a modified least-significant-bit scheme.
- **Video:** experimental single-frame embedding and extraction, with a user-provided key for the RC4 demonstration.

The image, text, and audio paths use a `*^*^*` end marker. Video uses the same marker after encrypting its message.

## Requirements

- Python 3.8 or later
- NumPy
- OpenCV for Python (`opencv-python`)
- For video support, an OpenCV build with a working video codec backend (the example writer requests XVID)

## Run the program

### 1. Get the project files

Download or clone this repository, then open a terminal in the project root (the folder containing `Steganography.py` and `requirements.txt`). The program uses paths relative to this folder, so run it from here.

```bash
git clone https://github.com/ShubxJha/steganography-methods.git
cd steganography-methods
```

If you already have the project downloaded, just change directory to its root instead.

### 2. Check Python

Install Python 3.8 or later if needed. Check that Python is available:

```bash
python --version
```

On some macOS/Linux systems, use `python3` in place of `python` in the commands below.

### 3. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install the dependencies

With the virtual environment active, install the packages listed in `requirements.txt`:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Image processing needs NumPy and OpenCV. The video option also needs an OpenCV build with a working codec backend; the program requests XVID when writing video.

### 5. Start the interactive menu

From the project root, run:

```bash
python Steganography.py
```

The main menu offers image, text, audio, and video steganography. Enter the number for the feature you want, then follow its prompts. Each feature has its own submenu; choose its exit option to return to the main menu, and choose `5` in the main menu to quit.

### 6. Encode a message

- **Image:** choose image steganography, then encode. The program loads `Sample_cover_files/cover_image.jpg`. Enter a message and an output filename ending in `.png` or `.bmp`. BPCS embeds data in 8×8 blocks across channel bit-planes; available capacity depends on image dimensions.
- **Text:** choose text steganography, then encode. The program uses `Sample_cover_files/cover_text.txt` as the cover and asks for the message and output filename.
- **Audio:** choose audio steganography, then encode. Enter the path to a WAV cover file, the message, and the output filename.
- **Video:** choose video steganography, then encode. It uses `Sample_cover_files/cover_video.mp4`, asks for a frame number, message, and key, and writes `stego_video.mp4` in the current folder. Video encoding is experimental; see [Limitations](#limitations).

### 7. Decode a message

Choose the same media type and its decode option. For image and text, provide the stego file path when prompted. For audio, enter the stego WAV path. For video, use the video submenu’s decode option in the same run as encoding and provide the frame number and key when asked; the current video implementation relies on in-memory frame state.

Keep stego files unchanged between encoding and decoding. For images, use the generated PNG or BMP file; JPEG, resizing, editing, or recompressing can corrupt the BPCS data. Decoded messages are displayed in the terminal.

## Limitations

- This is a demonstration, not encryption or secure communication. BPCS and zero-width-character hiding provide no confidentiality or integrity.
- BPCS uses a fixed complexity threshold of 0.3 and 8×8 blocks across all image channels and bit-planes. Capacity depends on image dimensions; use a lossless PNG or BMP output.
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

