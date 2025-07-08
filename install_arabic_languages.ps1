# Install Arabic Language Packs for Tesseract
# Run as Administrator

Write-Host "Installing Arabic Language Packs for Tesseract" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "ERROR: This script requires administrator privileges." -ForegroundColor Red
    Write-Host "Please run PowerShell as Administrator and try again." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

$tessdata = "C:\Program Files\Tesseract-OCR\tessdata"
$tempDir = "$env:TEMP\tesseract_langs"

# Ensure temp directory exists
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

# List of Arabic language files to download
$arabicFiles = @(
    "ara.traineddata",
    "osd.traineddata"
)

Write-Host "Downloading Arabic language files..." -ForegroundColor Yellow

foreach ($file in $arabicFiles) {
    $url = "https://github.com/tesseract-ocr/tessdata/raw/main/$file"
    $tempFile = "$tempDir\$file"
    $destFile = "$tessdata\$file"
    
    try {
        if (Test-Path $destFile) {
            Write-Host "✓ $file already exists" -ForegroundColor Green
            continue
        }
        
        Write-Host "Downloading $file..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri $url -OutFile $tempFile
        
        Write-Host "Installing $file..." -ForegroundColor Yellow
        Copy-Item $tempFile $destFile -Force
        
        Write-Host "✓ $file installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed to install $file : $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Clean up temp files
Write-Host ""
Write-Host "Cleaning up temporary files..." -ForegroundColor Yellow
Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue

# Verify installation
Write-Host ""
Write-Host "Verifying Arabic language support..." -ForegroundColor Yellow
try {
    $languages = & "C:\Program Files\Tesseract-OCR\tesseract.exe" --list-langs
    Write-Host "Available languages:" -ForegroundColor White
    $languages | ForEach-Object { Write-Host "  $_" -ForegroundColor White }
    
    if ($languages -contains "ara") {
        Write-Host ""
        Write-Host "✓ Arabic language support successfully installed!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "✗ Arabic language support not found. Please check installation." -ForegroundColor Red
    }
} catch {
    Write-Host "✗ Error checking language support: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Installation completed!" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit"
