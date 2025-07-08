@echo off
echo Setting up Python Arabic OCR Server...
echo.

REM Check if Python is installed first
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.8+ from: https://python.org
    echo.
    echo Installation options:
    echo 1. Download from https://python.org/downloads/
    echo 2. Install from Microsoft Store
    echo 3. Use Chocolatey: choco install python
    echo.
    echo After installing Python, run this setup again.
    echo.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%

REM Basic version check (this is simplified - full check is in setup.py)
echo %PYTHON_VERSION% | findstr "^3\.[8-9]\|^3\.[1-9][0-9]\|^[4-9]\." >nul
if %errorlevel% neq 0 (
    echo WARNING: Python %PYTHON_VERSION% found, but Python 3.8+ recommended
    echo The setup will continue but you may encounter issues.
    echo.
)

echo ✅ Python check passed
echo.

REM Check if Chocolatey is installed
echo Checking for Chocolatey...
choco --version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Chocolatey is not installed. Tesseract update will be skipped.
    echo To install Chocolatey, visit: https://chocolatey.org/install
    echo After installing Chocolatey, run this setup again for automatic Tesseract updates.
    echo.
    goto :python_setup
)

REM Install/Update Tesseract via Chocolatey
echo Installing/Updating Tesseract OCR to latest version via Chocolatey...
choco upgrade tesseract -y
if %errorlevel% neq 0 (
    echo WARNING: Failed to install/update Tesseract via Chocolatey.
    echo Please install Tesseract manually from: https://github.com/UB-Mannheim/tesseract/releases
    echo.
) else (
    echo Tesseract OCR installed/updated successfully to latest version.
    echo.
)

:python_setup
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing required packages...
pip install -r requirements.txt

echo.
echo Setup complete! You can now run start_server.bat to start the server.
pause
