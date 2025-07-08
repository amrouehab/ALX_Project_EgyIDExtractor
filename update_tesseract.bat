@echo off
echo Tesseract OCR Update Script
echo ===========================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo This script requires administrator privileges to update Tesseract.
    echo Please run as administrator for automatic updates.
    echo.
    pause
    exit /b 1
)

REM Check if Chocolatey is installed
echo Checking for Chocolatey...
choco --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Chocolatey is not installed.
    echo.
    echo Option 1: Install Chocolatey (Recommended for automatic updates)
    echo Run this command in an admin PowerShell:
    echo Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    echo.
    echo Option 2: Manual Tesseract Installation
    echo Download from: https://github.com/UB-Mannheim/tesseract/releases
    echo.
    pause
    exit /b 1
)

REM Show current Tesseract version if installed
echo Current Tesseract version:
"C:\Program Files\Tesseract-OCR\tesseract.exe" --version 2>nul || echo Tesseract not found in standard location
echo.

REM Update Tesseract via Chocolatey
echo Updating Tesseract OCR to latest version...
choco upgrade tesseract -y
if %errorlevel% neq 0 (
    echo Failed to update Tesseract via Chocolatey.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo Tesseract OCR updated successfully!
echo.

REM Show new version
echo New Tesseract version:
"C:\Program Files\Tesseract-OCR\tesseract.exe" --version 2>nul || echo Please restart your command prompt to refresh PATH
echo.

echo Update completed successfully!
pause
