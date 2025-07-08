# Python Arabic OCR Server

A powerful Flask-based REST API server for Arabic OCR (Optical Character Recognition) processing. This server provides automated text extraction from Arabic documents and ID cards with high accuracy.

## 🚀 Quick Start

### One-Command Installation

**Windows:**
```powershell
git clone <repository-url>
cd PythonArabicOCRServer
python setup.py
```

**Linux/macOS:**
```bash
git clone <repository-url>
cd PythonArabicOCRServer
chmod +x setup.sh && ./setup.sh
```

### Start the Server
```bash
# Windows
start_server.bat

# Linux/macOS  
./start_server.sh
```

**Server URL:** http://127.0.0.1:5000

## 📋 Prerequisites

- **Python 3.8+** (automatically verified)
- **Git** (to clone repository)
- **Tesseract OCR** (automatically installed)

*All dependencies are automatically installed by the setup scripts.*

## 📖 Full Documentation

For detailed installation instructions, troubleshooting, and advanced configuration:

👉 **[See INSTALLATION.md](INSTALLATION.md)**

## ✅ Verification

After setup, run the test script to verify everything is working:

```bash
# Windows
test_setup.bat

# Linux/macOS
./test_setup.sh
```

## 🔧 Manual Setup

If automatic setup fails, see the manual installation section in [INSTALLATION.md](INSTALLATION.md).

## 📁 Project Structure

- `RestAPI.py` - Main Flask application  
- `IDCroper.py` - ID card extraction utilities
- `IDModel.py` - ID processing models
- `OCRExtractor.py` - OCR extraction functionality
- `DBHelper.py` - Database helper functions
- `setup.py` - Cross-platform setup script
- `setup.bat/.sh` - Platform-specific setup scripts
- `start_server.bat/.sh` - Server startup scripts
- `test_setup.bat/.sh` - Setup verification scripts

## 🌐 API Endpoints

The server provides REST API endpoints for OCR processing. Key endpoints include:

- `GET /` - Server health check
- `POST /recognize-text/<char>/<threshold>` - OCR text recognition
- `POST /save/` - Save OCR results to database
- `POST /check-file/` - File processing status
- `POST /save-config/` - Configuration management

## 🔍 Features

- ✅ **Cross-platform support** (Windows, Linux, macOS)
- ✅ **Automated setup** with dependency management  
- ✅ **Arabic text recognition** with Tesseract OCR
- ✅ **ID card processing** with computer vision
- ✅ **RESTful API** with Flask
- ✅ **Database integration** (PostgreSQL, SQL Server)
- ✅ **Image preprocessing** with OpenCV
- ✅ **Configuration management**

## 🛠️ Development

For development setup:

1. Follow the installation guide
2. Activate virtual environment: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate.bat` (Windows)
3. Install additional dev dependencies if needed
4. The server runs in development mode by default

## 🚀 Production Deployment

For production deployment:

- Use a WSGI server like Gunicorn or Waitress
- Configure environment variables
- Set up reverse proxy (nginx/Apache)
- Enable SSL/TLS

See [INSTALLATION.md](INSTALLATION.md) for detailed production setup instructions.

## 🆘 Need Help?

1. **Check [INSTALLATION.md](INSTALLATION.md)** for detailed troubleshooting
2. **Run test scripts** to identify issues
3. **Check GitHub Issues** for known problems
4. **Create new issue** with full error details

## 📝 Requirements
## 📝 Requirements

All dependencies are automatically managed by the setup scripts. Core requirements include:

- Flask 3.0.2+ (Web framework)
- OpenCV 4.9.0+ (Computer vision)
- NumPy 1.26.4+ (Numerical computing) 
- Pillow 10.2.0+ (Image processing)
- pytesseract 0.3.10+ (OCR interface)
- Flask-CORS 4.0.0+ (Cross-origin requests)

*See `requirements.txt` or `requirements-cross-platform.txt` for complete dependency list.*

## 📄 License

[Add your license information here]

## 🤝 Contributing

[Add contribution guidelines here]

---

**Made with ❤️ for Arabic text processing**
