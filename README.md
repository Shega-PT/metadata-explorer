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

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/metadata-explorer.git
   cd metadata-explorer
