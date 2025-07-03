@echo off
echo Starting Python Arabic OCR Server...
echo.

REM Check if virtual environment exists
if not exist "Scripts\python.exe" (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

echo Activating virtual environment...
call Scripts\activate.bat

echo Starting Flask server...
python RestAPI.py

pause
