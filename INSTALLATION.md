# Installation Guide for Python Arabic OCR Server

This guide will help you set up the Python Arabic OCR Server on any operating system (Windows, Linux, or macOS).

## Quick Start

### Option 1: One-Command Setup (Recommended)

**Windows (PowerShell or Command Prompt):**
```powershell
git clone https://github.com/your-username/PythonArabicOCRServer.git
cd PythonArabicOCRServer
python setup.py
```

**Linux/macOS (Terminal):**
```bash
git clone https://github.com/your-username/PythonArabicOCRServer.git
cd PythonArabicOCRServer
chmod +x setup.sh
./setup.sh
```

### Option 2: Platform-Specific Scripts

**Windows:**
```batch
git clone https://github.com/your-username/PythonArabicOCRServer.git
cd PythonArabicOCRServer
setup.bat
```

**Linux/macOS:**
```bash
git clone https://github.com/your-username/PythonArabicOCRServer.git
cd PythonArabicOCRServer
chmod +x setup.sh
./setup.sh
```

## What the Setup Does

The automated setup will:

1. ✅ Check Python 3.8+ installation
2. ✅ Install/update Tesseract OCR with Arabic language support
3. ✅ Create a Python virtual environment
4. ✅ Install all required Python packages
5. ✅ Create platform-specific startup scripts
6. ✅ Verify the installation

## Prerequisites

### Required (Auto-installed by setup)
- **Python 3.8 or higher**
- **Tesseract OCR** with Arabic language pack
- **Git** (to clone the repository)

### Windows Prerequisites
- **Windows 10/11**
- **PowerShell** or **Command Prompt**
- **Python** from [python.org](https://python.org) or Microsoft Store
- **Git** from [git-scm.com](https://git-scm.com)

*Optional: [Chocolatey](https://chocolatey.org) for automatic Tesseract installation*

### Linux Prerequisites (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git
```

### Linux Prerequisites (CentOS/RHEL/Fedora)
```bash
# CentOS/RHEL
sudo yum install python3 python3-pip git

# Fedora
sudo dnf install python3 python3-pip git
```

### macOS Prerequisites
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and Git
brew install python3 git
```

## Step-by-Step Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/PythonArabicOCRServer.git
cd PythonArabicOCRServer
```

### Step 2: Run Setup
Choose one of the setup methods based on your system:

**Cross-Platform Python Setup:**
```bash
python setup.py    # Windows
python3 setup.py   # Linux/macOS
```

**Windows Batch Script:**
```batch
setup.bat
```

**Linux/macOS Shell Script:**
```bash
chmod +x setup.sh
./setup.sh
```

### Step 3: Verify Installation
**Windows:**
```batch
test_setup.bat
```

**Linux/macOS:**
```bash
chmod +x test_setup.sh
./test_setup.sh
```

### Step 4: Start the Server
**Windows:**
```batch
start_server.bat
```

**Linux/macOS:**
```bash
./start_server.sh
```

**Or manually:**
```bash
# Activate virtual environment
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate.bat   # Windows

# Start server
python RestAPI.py
```

## Verification

After setup, the server should be accessible at: **http://127.0.0.1:5000**

You should see: "OCR Server is running..."

## Troubleshooting

### Common Issues and Solutions

#### 1. Python Not Found
**Error:** `python: command not found`

**Solutions:**
- **Windows:** Install Python from [python.org](https://python.org) and ensure "Add to PATH" is checked
- **Linux:** `sudo apt install python3` (Ubuntu) or `sudo yum install python3` (CentOS)
- **macOS:** `brew install python3`
- Try using `python3` instead of `python`

#### 2. Tesseract Not Found
**Error:** `tesseract: command not found`

**Solutions:**
- **Windows:** 
  - Install Chocolatey: `Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))`
  - Then: `choco install tesseract -y`
  - Or download manually from [GitHub](https://github.com/UB-Mannheim/tesseract/releases)
- **Linux:** `sudo apt install tesseract-ocr tesseract-ocr-ara`
- **macOS:** `brew install tesseract tesseract-lang`

#### 3. Arabic Language Pack Missing
**Error:** `tesseract --list-langs` doesn't show 'ara'

**Solutions:**
- **Windows:** Run `install_arabic_languages.ps1` script
- **Linux:** `sudo apt install tesseract-ocr-ara`
- **macOS:** Arabic is included with `tesseract-lang`

#### 4. Permission Denied (Linux/macOS)
**Error:** `Permission denied: ./setup.sh`

**Solution:**
```bash
chmod +x setup.sh start_server.sh test_setup.sh
```

#### 5. Virtual Environment Issues
**Error:** Virtual environment creation fails

**Solution:**
```bash
# Delete existing venv and try again
rm -rf venv        # Linux/macOS
rmdir /s venv      # Windows

# Ensure python3-venv is installed (Linux)
sudo apt install python3-venv
```

#### 6. Package Installation Fails
**Error:** `pip install` fails

**Solutions:**
- Update pip: `python -m pip install --upgrade pip`
- Check internet connection
- Try: `pip install --user -r requirements.txt`
- On Linux, install system dependencies: `sudo apt install python3-dev build-essential`

#### 7. OpenCV Issues (Linux)
**Error:** OpenCV import fails

**Solution:**
```bash
sudo apt install python3-opencv libopencv-dev
```

#### 8. Database Connection Issues
**Error:** Database connection fails

**Solutions:**
- **PostgreSQL:** Ensure PostgreSQL is installed and running
- **SQL Server:** Only supported on Windows with SQL Server
- Check connection strings in the code

### Manual Tesseract Installation

If automatic installation fails:

#### Windows Manual Installation
1. Download from: https://github.com/UB-Mannheim/tesseract/releases
2. Install to default location (usually `C:\Program Files\Tesseract-OCR`)
3. Add to PATH environment variable
4. Download Arabic language pack (`ara.traineddata`) to tessdata folder

#### Linux Manual Installation
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-ara libtesseract-dev

# CentOS/RHEL
sudo yum install tesseract tesseract-langpack-ara

# Fedora
sudo dnf install tesseract tesseract-langpack-ara
```

#### macOS Manual Installation
```bash
brew install tesseract tesseract-lang
```

## Advanced Configuration

### Production Deployment
For production use, consider:

1. **Use a production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 RestAPI:app
   ```

2. **Set environment variables:**
   - Database connection strings
   - Secret keys
   - Debug mode (set to False)

3. **Configure reverse proxy (nginx/Apache)**

4. **Set up SSL/TLS certificates**

### Environment Variables
Create a `.env` file for configuration:
```env
FLASK_ENV=production
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
```

## Getting Help

If you encounter issues not covered here:

1. Check the error messages carefully
2. Ensure all prerequisites are installed
3. Try running the test script: `test_setup.bat` or `test_setup.sh`
4. Check the project's GitHub issues page
5. Create a new issue with:
   - Your operating system
   - Python version (`python --version`)
   - Full error message
   - Steps you've tried

## Project Structure

After successful setup, you'll have:

```
PythonArabicOCRServer/
├── venv/                          # Virtual environment
├── RestAPI.py                     # Main Flask application
├── requirements.txt               # Python dependencies
├── setup.py                       # Cross-platform setup script
├── setup.bat                      # Windows setup script
├── setup.sh                       # Linux/macOS setup script
├── start_server.bat              # Windows server start
├── start_server.sh               # Linux/macOS server start
├── test_setup.bat                # Windows test script
├── test_setup.sh                 # Linux/macOS test script
├── README.md                     # Project documentation
└── [other project files...]
```

## Success Indicators

✅ **Setup is successful when:**
- All test scripts pass
- Server starts without errors
- http://127.0.0.1:5000 shows "OCR Server is running..."
- Tesseract version displays correctly
- Arabic language support is confirmed

Happy coding! 🚀
