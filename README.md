# Python Arabic OCR Server

This is a Flask-based REST API server for Arabic OCR (Optical Character Recognition) processing.

## Setup Instructions

### Prerequisites
- Python 3.12 or higher
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd PythonArabicOCRServer
   ```

2. **Create a Python virtual environment:**
   ```bash
   python -m venv .
   ```

3. **Activate the virtual environment:**
   
   **On Windows:**
   ```powershell
   .\Scripts\Activate.ps1
   ```
   
   **On Linux/Mac:**
   ```bash
   source bin/activate
   ```

4. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Server

1. **Make sure you're in the project directory and virtual environment is activated**

2. **Run the Flask server:**
   ```bash
   python RestAPI.py
   ```

3. **The server will start on:**
   ```
   http://127.0.0.1:5000
   ```

## Project Structure

- `RestAPI.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `IDCroper.py` - ID card extraction utilities
- `IDModel.py` - ID processing models
- `OCRExtractor.py` - OCR extraction functionality
- `DBHelper.py` - Database helper functions
- `.gitignore` - Git ignore rules

## API Endpoints

The server provides endpoints for OCR processing. Check the `RestAPI.py` file for specific endpoint details.

## Development

- The server runs in development mode by default
- For production deployment, use a proper WSGI server like Gunicorn or Waitress
- Make sure to configure proper environment variables for production

## Notes

- This project uses Tesseract OCR for text extraction
- OpenCV is used for image processing
- Flask provides the REST API interface
