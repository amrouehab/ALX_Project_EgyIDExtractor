@echo off
echo Setting up Python Arabic OCR Server...
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
