@echo off
echo Tesseract Version Check
echo ======================
echo.

echo Current Tesseract version:
"C:\Program Files\Tesseract-OCR\tesseract.exe" --version 2>nul
if %errorlevel% neq 0 (
    echo Tesseract not found in standard location.
    echo Please install Tesseract OCR.
)

echo.
echo Checking Chocolatey version:
choco --version 2>nul
if %errorlevel% neq 0 (
    echo Chocolatey not found. Install from: https://chocolatey.org/install
) else (
    echo Chocolatey found. You can use: choco upgrade tesseract -y
)

echo.
echo Arabic language support check:
"C:\Program Files\Tesseract-OCR\tesseract.exe" --list-langs 2>nul | findstr ara
if %errorlevel% neq 0 (
    echo Arabic language packs not found or Tesseract not installed.
)

echo.
echo To update Tesseract, run as Administrator:
echo   update_tesseract.bat  or  update_tesseract.ps1
echo.
pause
