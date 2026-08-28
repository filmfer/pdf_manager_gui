# simple PDF Manager

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Platform: Windows & macOS](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-blue.svg)](#-download)
[![GUI: Tkinter](https://img.shields.io/badge/GUI-Tkinter-0078d4.svg)](https://docs.python.org/3/library/tkinter.html)
[![PDF: pypdf](https://img.shields.io/badge/PDF-pypdf-ff6b35.svg)](https://pypdf.readthedocs.io/)
[![Image: Pillow](https://img.shields.io/badge/Image-Pillow-669900.svg)](https://python-pillow.org/)
[![Render: PyMuPDF](https://img.shields.io/badge/Render-PyMuPDF-ff8c00.svg)](https://pymupdf.readthedocs.io/)

> **simple PDF Manager** — A free, portable, lightweight GUI tool for everyday
> PDF tasks. Merge, split, extract, remove pages, create PDFs from images, and
> export PDF pages to images — all in one clean, no-installation application
> built with Python, Tkinter, pypdf, Pillow, and PyMuPDF.

---

## Table of Contents

- [✨ Features](#-features)
- [📸 Demo Screenshots](#-demo-screenshots)
- [📦 Download](#-download)
- [🚀 Quick Start](#-quick-start)
- [🔧 Build from Source](#-build-from-source)
- [📖 Usage Guide](#-usage-guide)
- [🛠️ Technical Details](#-technical-details)
- [📄 License](#-license)

---

## ✨ Features

| Feature | What It Does |
|---------|-------------|
| **Merge PDFs** | Combine two or more PDF files into a single document |
| **Extract Pages** | Pull specific page ranges from a PDF into a new file |
| **Remove Pages** | Delete unwanted pages and save the cleaned PDF |
| **Split PDF** | Split a PDF into individual single-page files |
| **Images → PDF** | Create a PDF from selected images or all images in a folder |
| **PDF → Images** | Export one or more PDF pages to PNG, JPEG, WEBP, TIFF, BMP |

### Supported Image Formats (Images → PDF)

**Input:** PNG, JPG, JPEG, JPE, JFIF, GIF, BMP, DIB, TIFF, TIF, WEBP, ICO,
PPM, PGM, PBM, PCX, TGA, SGI, XBM, XPM, QOI

**Output (PDF → Images):** PNG, JPEG, WEBP, TIFF, BMP, PPM, PGM, PBM

---

## 📦 Download

Pre-built portable applications are available in the **[GitHub Releases](https://github.com/filmfer/pdf_manager_gui/releases)** page or under **Actions -> Artifacts**.

- **Windows:** Download `simple PDF Manager.exe`
- **macOS (Apple Silicon M-Series):** Download the `.dmg` installer or the `.app` bundle

Simply download the version for your operating system and run it. No Python installation is required!

---

## 🚀 Quick Start

### Using the Portable Application

1. Go to the **[Releases](https://github.com/filmfer/pdf_manager_gui/releases)** page and download the `.exe` (Windows) or `.dmg` (Mac).
2. **Windows:** Double-click the `.exe` to run.
3. **macOS:** Open the `.dmg` and drag the App to your Applications folder, then launch it.
4. Click any feature button and follow the on-screen dialogs!

### Running from Source

```bash
# Clone the repository
git clone https://github.com/filmfer/simple-pdf-manager.git
cd simple-pdf-manager

# Install dependencies
pip install -r requirements.txt

# Launch the application
python pdf_manager.py
```

---

## 📖 Usage Guide

### Merge PDFs
1. Click **Merge PDFs**
2. Select two or more PDF files
3. Choose where to save the merged result

### Extract Pages
1. Click **Extract Pages**
2. Select a PDF file
3. Enter the start and end page numbers
4. Save the extracted pages as a new PDF

### Remove Pages
1. Click **Remove Pages**
2. Select a PDF file
3. Enter page numbers to remove (comma-separated, e.g., `1,3,5`)
4. Save the modified PDF

### Split PDF
1. Click **Split PDF: one file per page**
2. Select a PDF file
3. Choose an output folder
4. Each page becomes a separate PDF file

### Create PDF from Images
1. Click **Create PDF from Images**
2. Choose **Yes** to use all images in a folder, or **No** to pick files
3. Select the output PDF file
4. One PDF page is created per image

### Export Pages to Images
1. Click **Export Pages to Images**
2. Select a PDF file
3. Set start/end pages, DPI resolution (50–600), and image format
4. Choose an output folder — each page is saved as a separate image

---

## 🖥️ Command-Line Interface (CLI)

The application now supports a powerful command-line interface. This means you can use the same `simple PDF Manager.exe` (or `python pdf_manager.py`) directly from a terminal like **PowerShell**, **CMD**, or **macOS Terminal**.
When you pass any command/argument, the app runs in CLI mode. When you launch it with no arguments, it opens the GUI normally.

> **Note for Windows:** The executable name contains spaces (`simple PDF Manager.exe`). When using it in a terminal, you must wrap the path in quotes, e.g. `".\simple PDF Manager.exe" merge ...`.

### General Syntax

```bash
".\simple PDF Manager.exe" <command> [options]
# or, if installed from source:
python pdf_manager.py <command> [options]
```

### Available Commands

#### `merge` — Merge PDFs

```bash
".\simple PDF Manager.exe" merge file1.pdf file2.pdf file3.pdf --output merged.pdf
```

#### `split` — Split into single pages

```bash
".\simple PDF Manager.exe" split document.pdf --output-dir ./pages
```

#### `extract` — Extract a page range

```bash
".\simple PDF Manager.exe" extract document.pdf --start 1 --end 5 --output part.pdf
```

#### `remove` — Remove pages (supports ranges)

```bash
".\simple PDF Manager.exe" remove document.pdf --pages 1,3,5-7 --output cleaned.pdf
```

#### `img2pdf` — Create PDF from images

```bash
".\simple PDF Manager.exe" img2pdf photo1.png photo2.jpg --output images.pdf
```

#### `pdf2img` — Export PDF pages to images

```bash
".\simple PDF Manager.exe" pdf2img document.pdf --start 1 --end 3 --dpi 300 --format .png --output-dir ./images
```

### CLI Options Summary

| Command | Argument | Required | Description |
|--------|----------|----------|-------------|
| `merge` | `files` | ✅ | Input PDF files in order |
| | `-o, --output` | ✅ | Output merged PDF file |
| `split` | `input` | ✅ | Input PDF file |
| | `-o, --output-dir` | ✅ | Output directory for single pages |
| `extract` | `input` | ✅ | Input PDF file |
| | `-s, --start` | ✅ | Start page number (1-based) |
| | `-e, --end` | ✅ | End page number (1-based) |
| | `-o, --output` | ✅ | Output PDF file |
| `remove` | `input` | ✅ | Input PDF file |
| | `-p, --pages` | ✅ | Comma-separated pages/ranges to remove (e.g. `1,3,5-7`) |
| | `-o, --output` | ✅ | Output PDF file |
| `img2pdf` | `images` | ✅ | Input image files |
| | `-o, --output` | ✅ | Output PDF file |
| `pdf2img` | `input` | ✅ | Input PDF file |
| | `-s, --start` | ❌ | Start page (default: `1`) |
| | `-e, --end` | ❌ | End page (default: last page) |
| | `-d, --dpi` | ❌ | Resolution 50-600 (default: `150`) |
| | `-f, --format` | ❌ | Image format (default: `.png`) |
| | `-o, --output-dir` | ✅ | Output directory |

---

## 🔧 Build from Source (Creating the .exe)

> Requires Python 3.8+ and [PyInstaller](https://pyinstaller.org/)

```bash
# Install build dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build the standalone executable
python -m PyInstaller "simple_pdf_manager.spec" --noconfirm --clean

# The executable will be in dist/simple PDF Manager.exe
```

### Build Optimization

The `.spec` file includes an extensive `excludes` list to prevent bundling
unnecessary packages (e.g., numpy, pandas, scipy, pydantic, cryptography,
langchain, etc.), keeping the final executable under ~35 MB.

---

## 🛠️ Technical Details

- **GUI Framework:** Tkinter (built-in with Python, no external dependencies)
- **PDF Library:** pypdf (merge, split, extract, remove pages)
- **Imaging:** Pillow (image decoding, images → PDF)
- **Rendering:** PyMuPDF / MuPDF (PDF pages → images)
- **Architecture:** Object-oriented, class-based design with modal dialogs
- **Cross-Platform:** Source runs on Windows, macOS, Linux (Standalone apps available for Windows and macOS M-Series)
- **No Long Path Issues:** Uses standard library path handling

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| OS | Windows 7 64-bit | Windows 10/11 64-bit |
| RAM | 2 GB | 4 GB+ |
| Disk Space | 35 MB | 50 MB+ |
| Python | 3.8+ | 3.11+ |

---

## 📄 License

This tool is provided as-is for personal and professional use.

The application uses open-source libraries under the following licenses:
- **Tkinter** — Python Software Foundation License (PSF)
- **pypdf** — MIT License

---

## 👤 Author

**Filipe Fernandes**
📧 filmfer@gmail.com

---

## ⭐ Support

If you find this tool useful, please consider:
- ⭐ Starring the repository
- 🍴 Forking for your own needs
- 📢 Sharing with colleagues

[![GitHub stars](https://img.shields.io/github/stars/filmfer/simple-pdf-manager?style=social)](https://github.com/filmfer/simple-pdf-manager)

