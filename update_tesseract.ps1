# Tesseract OCR Update Script (PowerShell)
# Run this script as Administrator for automatic Tesseract updates

Write-Host "Tesseract OCR Update Script" -ForegroundColor Cyan
Write-Host "===========================" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "ERROR: This script requires administrator privileges." -ForegroundColor Red
    Write-Host "Please run PowerShell as Administrator and try again." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Chocolatey is installed
Write-Host "Checking for Chocolatey..." -ForegroundColor Yellow
try {
    $chocoVersion = choco --version 2>$null
    Write-Host "Chocolatey found: $chocoVersion" -ForegroundColor Green
} catch {
    Write-Host "Chocolatey is not installed." -ForegroundColor Red
    Write-Host ""
    Write-Host "Installing Chocolatey..." -ForegroundColor Yellow
    
    # Install Chocolatey
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    try {
        iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        Write-Host "Chocolatey installed successfully!" -ForegroundColor Green
        
        # Refresh environment variables
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    } catch {
        Write-Host "Failed to install Chocolatey. Please install manually from https://chocolatey.org/install" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Show current Tesseract version if installed
Write-Host ""
Write-Host "Current Tesseract version:" -ForegroundColor Yellow
try {
    $currentVersion = & "C:\Program Files\Tesseract-OCR\tesseract.exe" --version 2>$null
    Write-Host $currentVersion -ForegroundColor White
} catch {
    Write-Host "Tesseract not found in standard location" -ForegroundColor Red
}

# Update Tesseract via Chocolatey
Write-Host ""
Write-Host "Updating Tesseract OCR to latest version..." -ForegroundColor Yellow
try {
    choco upgrade tesseract -y
    Write-Host "Tesseract OCR updated successfully!" -ForegroundColor Green
} catch {
    Write-Host "Failed to update Tesseract via Chocolatey." -ForegroundColor Red
    Write-Host "Please check your internet connection and try again." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Show new version
Write-Host ""
Write-Host "New Tesseract version:" -ForegroundColor Yellow
try {
    # Refresh PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    $newVersion = & "C:\Program Files\Tesseract-OCR\tesseract.exe" --version 2>$null
    Write-Host $newVersion -ForegroundColor White
} catch {
    Write-Host "Please restart your command prompt to refresh PATH" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Update completed successfully!" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit"
