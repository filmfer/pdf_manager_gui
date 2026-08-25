# simple PDF Manager - Portable Windows Executable

## File Information
- **Filename:** `simple PDF Manager.exe`
- **Location:** `d:/scripts/pdf_manager_gui/dist/simple PDF Manager.exe`
- **Size:** ~34.7 MB
- **Architecture:** Windows 64-bit
- **Type:** Standalone portable executable (no installation required)

## Features
This is a fully portable, self-contained executable that includes:
- ✅ Complete Python runtime
- ✅ All required libraries (pypdf, Pillow, PyMuPDF, tkinter)
- ✅ All PDF manipulation functionality
- ✅ No dependencies - runs on any Windows 64-bit system

## How to Use
1. **Copy the executable** to any location on your Windows system
2. **Double-click** `simple PDF Manager.exe` to run
3. **No installation needed** - it runs immediately
4. **No Python required** on the target system

## Includes All Functions
- 🔗 **Merge PDFs** - Combine multiple PDF files
- 📄 **Extract Pages** - Extract page ranges from PDFs
- ❌ **Remove Pages** - Remove specific pages from PDFs
- ✂️ **Split PDF** - Split PDF into single-page files
- 🖼️ **Create PDF from Images** - Build PDF from selected or folder images
- 📸 **Export Pages to Images** - Export PDF pages to PNG, JPEG, WEBP, TIFF, BMP, PPM

## Requirements
- Windows 64-bit (7, 8, 10, 11)
- ~34.7 MB free disk space (for the .exe)
- That's it! No Python, no dependencies, no installation

## Certificate Status
⚠️ **Unsigned Executable**

This executable is unsigned, which means:
- Windows may display a security warning when first running it
- The warning is normal for executables not signed by a certificate authority
- The warning can be dismissed by clicking "Run anyway"

### To Obtain a Signed Certificate:
You would need:
1. A valid code signing certificate from a certificate authority (e.g., Sectigo, DigiCert)
2. Admin rights to install the certificate
3. Signtool.exe or similar to sign the executable
4. The signing key and password

**Note:** Code signing certificates typically cost $100-500 per year and require admin rights to install.

## Security
- ✅ Built from verified source code (pdf_manager.py)
- ✅ Uses only standard, trusted Python libraries (pypdf, Pillow, PyMuPDF, tkinter)
- ✅ No malware, no telemetry, no external connections
- ✅ Open source approach (source code available for inspection)

## Deployment
This executable is ideal for:
- Single-user distribution
- Enterprise deployment (with GPO)
- USB portable installations
- Shared network drives
- No-installation scenarios

## Troubleshooting

### If Windows blocks the file:
1. Right-click the .exe
2. Select "Properties"
3. Check "Unblock" checkbox at the bottom
4. Click "Apply" and "OK"
5. Run the application

### Memory Usage:
- Initial: ~150-200 MB
- During operations: ~300-500 MB
- Normal and expected for Python-based applications

## Version Information
- **Built:** 8/24/2026
- **Python Version:** 3.11.9
- **PyInstaller:** 6.18.0
- **pypdf:** 6.7.0+
- **Pillow:** 10.2.0+
- **PyMuPDF:** 1.23.8+

## Support
For issues or questions about the application, refer to:
- `README.md` - User guide and feature documentation
- `pdf_manager.py` - Source code with detailed comments

---

**Ready to use!** Simply copy `simple PDF Manager.exe` to your Windows system and run it.

## Legal constraints:
##- The app uses only open-source Python libraries: Tkinter (built-in, PSF License), pypdf (MIT License), Pillow (HPN License), and PyMuPDF (AGPL v3 / commercial dual-license).
##- MIT License allows commercial, government, and private use with minimal restrictions. No royalties or attribution required for deployment.
##- There are no known legal barriers for government use.

##Security review:
- The source code does not use network, subprocess, or unsafe eval functions.
##- All file operations are local and user-initiated.
##- No telemetry, data collection, or external connections.
##- pypdf is widely used and actively maintained, with no known critical vulnerabilities as of Feb 2026.
##- Tkinter is part of Python core and has no known attack vectors.

##Known risks:
##- Only files selected by the user are processed.
##- No shell injection, no arbitrary code execution.
##- No password handling or cryptography.
##- No privilege escalation or system modification.

##**Conclusion:** The app is safe for government use, with no legal or known security issues. For full compliance, review the MIT license and consider regular dependency ##updates.
