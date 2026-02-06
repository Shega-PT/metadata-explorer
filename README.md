# 🔍 Metadata Explorer

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

A powerful, cross-platform Python tool for deep metadata extraction from various file types. Perfect for digital forensics, organization, and curiosity!

## ✨ Features

- **🔍 Deep Metadata Extraction** - Supports images (EXIF), audio (ID3), and video files
- **📁 Recursive Scanning** - Explores entire directory structures
- **📊 Detailed Reports** - Generates comprehensive metadata logs
- **🚀 Cross-Platform** - Works on Windows, macOS, and Linux
- **🛡️ Error Resilient** - Continues scanning even if some files fail
- **📈 Smart Filtering** - Automatically skips system files and directories

## 📁 Supported Formats

| Category | Formats | Metadata Extracted |
|----------|---------|-------------------|
| **Images** | JPG, PNG, HEIC, TIFF, WebP, BMP, GIF | EXIF, GPS, Camera settings, Timestamps |
| **Audio** | MP3, FLAC, M4A, OGG, WAV, AAC | ID3 tags, Duration, Bitrate, Codec info |
| **Video** | MP4, MOV, AVI, MKV, WMV | Duration, Resolution, Codec, Creation date |
| **All Files** | Any file type | Size, Creation/modification dates, Path |


## 🚀 Quick Start

### Installation

1. Clone the repository:

   git clone https://github.com/yourusername/metadata-explorer.git
   cd metadata-explorer


2. Install dependencies:

pip install -r requirements.txt


Basic Usage
Scan the current directory:

python universal.py


Scan a specific directory:

python universal.py /path/to/your/files


Scan your entire pictures folder:

python universal.py ~/Pictures



📊 Example Output

text
============================================================
DIRECTORY: Vacation_Photos
============================================================

FILE: beach_sunset.jpg
PATH: Vacation_Photos/beach_sunset.jpg
METADATA:
  • IMG_EXIF_DateTimeOriginal: 2023:07:15 18:32:45
  • IMG_GPSInfo: GPSLatitudeRef: N, GPSLatitude: [38, 43, 23.4]...
  • IMG_Image_Make: Canon
  • IMG_Image_Model: Canon EOS R5
  • FILE_SIZE: 8456723 bytes
  • CREATED: 1692067565.12345

  
🛠️ Advanced Usage
Customizing Ignored Files
Edit the ignored_dirs and ignored_files sets in the FileManager class to customize what gets skipped.

Output to Different Format
The script outputs to metadata_report.log by default. Modify setup_logging() to change the output format or location.

Integrating with Other Tools
Use the UniversalMetadataExtractor class independently in your projects:

python
from pathlib import Path
from universal import UniversalMetadataExtractor

extractor = UniversalMetadataExtractor()
metadata = extractor.get_all_metadata(Path("your_file.jpg"))
print(metadata["IMG_EXIF_DateTimeOriginal"])


📁 Project Structure

metadata-explorer/
├── universal.py          # Main script
├── requirements.txt      # Dependencies
├── README.md            # This file
├── metadata_report.log  # Generated report (example)
└── examples/
    └── sample_scan/     # Example directory structure

    
🤝 Contributing

Contributions are welcome! Here's how you can help:

Report Bugs - Open an issue with detailed information
Suggest Features - Share your ideas for improvements
Submit Pull Requests - Add support for new file formats or features

Development Setup
Clone and install in development mode

git clone https://github.com/yourusername/metadata-explorer.git
cd metadata-explorer
pip install -e .
pip install -r requirements-dev.txt  # Optional dev dependencies

🙏 Acknowledgments

exifread for EXIF data extraction
mutagen for audio metadata
hachoir for video metadata analysis
Pillow for image processing capabilities

⚠️ Disclaimer

This tool is for educational and organizational purposes only. Always respect privacy laws and obtain proper permissions before scanning others' files.


Made with ❤️ for digital explorers everywhere
⭐ If you find this useful, please consider starring the repository!
