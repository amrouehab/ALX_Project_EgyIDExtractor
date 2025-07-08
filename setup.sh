#!/bin/bash

# Python Arabic OCR Server Setup Script for Linux/macOS
# This script sets up the OCR server with all dependencies

set -e  # Exit on any error

echo "==============================================="
echo "Python Arabic OCR Server Setup (Linux/macOS)"
echo "==============================================="
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
print_status "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    echo "Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip python3-venv"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "macOS: brew install python3"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
print_success "Python $PYTHON_VERSION found"

# Check if pip is installed
print_status "Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip."
    exit 1
fi

# Install/Update Tesseract OCR
print_status "Installing/Updating Tesseract OCR..."

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v apt &> /dev/null; then
        # Ubuntu/Debian
        print_status "Detected Ubuntu/Debian system"
        sudo apt update
        sudo apt install -y tesseract-ocr tesseract-ocr-ara libtesseract-dev
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL
        print_status "Detected CentOS/RHEL system"
        sudo yum install -y tesseract tesseract-langpack-ara tesseract-devel
    elif command -v dnf &> /dev/null; then
        # Fedora
        print_status "Detected Fedora system"
        sudo dnf install -y tesseract tesseract-langpack-ara tesseract-devel
    elif command -v pacman &> /dev/null; then
        # Arch Linux
        print_status "Detected Arch Linux system"
        sudo pacman -S --noconfirm tesseract tesseract-data-ara
    else
        print_warning "Unknown Linux distribution. Please install Tesseract manually:"
        print_warning "Visit: https://tesseract-ocr.github.io/tessdoc/Installation.html"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    print_status "Detected macOS system"
    if command -v brew &> /dev/null; then
        brew install tesseract tesseract-lang
        print_success "Tesseract installed via Homebrew"
    else
        print_warning "Homebrew not found. Please install Homebrew first:"
        print_warning '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        print_warning "Then run: brew install tesseract tesseract-lang"
    fi
fi

# Verify Tesseract installation
if command -v tesseract &> /dev/null; then
    TESSERACT_VERSION=$(tesseract --version | head -n1)
    print_success "Tesseract found: $TESSERACT_VERSION"
    
    # Check Arabic language support
    if tesseract --list-langs | grep -q "ara"; then
        print_success "Arabic language support confirmed"
    else
        print_warning "Arabic language pack not found. Some features may not work."
    fi
else
    print_error "Tesseract installation failed. Please install manually."
fi

# Create Python virtual environment
print_status "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
print_status "Installing Python dependencies..."

# Check for cross-platform requirements first
if [ -f "requirements-cross-platform.txt" ]; then
    print_status "Using cross-platform requirements file"
    pip install -r requirements-cross-platform.txt
elif [ -f "requirements.txt" ]; then
    print_status "Using standard requirements file"
    # Install requirements but skip Windows-specific packages
    pip install -r requirements.txt 2>/dev/null || {
        print_warning "Some packages failed to install. Trying individual installation..."
        while IFS= read -r line; do
            # Skip empty lines and comments
            if [[ -z "$line" || "$line" =~ ^#.* ]]; then
                continue
            fi
            
            # Skip Windows-specific packages
            if [[ "$line" =~ pywin32 || "$line" =~ pyodbc ]]; then
                print_status "Skipping Windows-specific package: $line"
                continue
            fi
            
            # Install package
            pip install "$line" || print_warning "Failed to install: $line"
        done < requirements.txt
    }
else
    print_error "No requirements file found!"
    exit 1
fi

print_success "Python dependencies installed successfully"

# Install additional system dependencies for OpenCV
print_status "Installing system dependencies for OpenCV..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v apt &> /dev/null; then
        sudo apt install -y python3-opencv libopencv-dev
    elif command -v yum &> /dev/null; then
        sudo yum install -y opencv opencv-python
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y opencv opencv-python
    fi
fi

# Create start script
print_status "Creating start script..."
cat > start_server.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
python RestAPI.py
EOF
chmod +x start_server.sh

print_success "Setup completed successfully!"
echo
echo "==============================================="
echo "Setup Summary:"
echo "✓ Python environment created in 'venv/'"
echo "✓ Dependencies installed"
echo "✓ Tesseract OCR configured"
echo "✓ Start script created"
echo "==============================================="
echo
echo "To start the server:"
echo "  ./start_server.sh"
echo
echo "Or manually:"
echo "  source venv/bin/activate"
echo "  python RestAPI.py"
echo
