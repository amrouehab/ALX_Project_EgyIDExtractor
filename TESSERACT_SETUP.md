# Tesseract OCR Installation & Update Guide

## Overview
This project uses Tesseract OCR for Arabic text recognition. To ensure optimal performance, we recommend always using the latest version of Tesseract.

## Automatic Installation (Recommended)

### Prerequisites
1. **Install Chocolatey** (Windows Package Manager):
   ```powershell
   # Run in Administrator PowerShell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

### Automated Setup
1. **Run setup script as Administrator:**
   ```batch
   setup.bat
   ```

This will automatically:
- ✅ Install/update Tesseract OCR to latest version
- ✅ Create Python virtual environment
- ✅ Install all Python dependencies
- ✅ Configure everything for immediate use

## Manual Installation

### Option 1: Chocolatey (Recommended)
```powershell
# Run as Administrator
choco install tesseract -y
```

### Option 2: Direct Download
1. Visit: https://github.com/UB-Mannheim/tesseract/releases
2. Download latest Windows installer (e.g., `tesseract-ocr-w64-setup-5.3.3.20231005.exe`)
3. Run installer with default settings
4. Ensure installation path is: `C:\Program Files\Tesseract-OCR\`

## Keeping Tesseract Updated

### Automatic Update Scripts
We provide two update scripts:

**PowerShell (Recommended):**
```powershell
# Run as Administrator
.\update_tesseract.ps1
```

**Batch:**
```batch
# Run as Administrator
update_tesseract.bat
```

### Manual Update via Chocolatey
```powershell
# Run as Administrator
choco upgrade tesseract -y
```

## Verification

Check your Tesseract installation:

```batch
# Check version
tesseract --version

# Check Arabic language support
tesseract --list-langs | findstr ara
```

Expected output should include:
- `ara` - Standard Arabic
- `ara-amiri-3000` - Amiri font support
- Other Arabic variants

## Troubleshooting

### Tesseract Not Found
1. Verify installation path: `C:\Program Files\Tesseract-OCR\`
2. Check PATH environment variable
3. Restart command prompt/PowerShell

### Permission Issues
- Always run update scripts as Administrator
- Ensure antivirus doesn't block Chocolatey

### Arabic Language Pack Missing
If Arabic text recognition fails:
```powershell
# Reinstall with language packs
choco uninstall tesseract -y
choco install tesseract -y
```

## Current Setup
- **Tesseract Version**: 5.3.3 (will be updated to latest)
- **Arabic Models**: Multiple specialized models included
- **Auto-Update**: Configured via Chocolatey

## Notes
- Tesseract 5.x provides significantly better Arabic OCR accuracy than 4.x
- The project includes specialized Arabic models for ID cards
- Regular updates ensure compatibility with latest Arabic fonts and text styles
