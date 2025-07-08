#!/usr/bin/env python3
"""
Cross-platform setup script for Python Arabic OCR Server
Works on Windows, Linux, and macOS
"""

import os
import sys
import subprocess
import platform
import venv
from pathlib import Path

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color
    
    @staticmethod
    def disable_on_windows():
        if platform.system() == "Windows":
            Colors.RED = Colors.GREEN = Colors.YELLOW = Colors.BLUE = Colors.NC = ""

# Disable colors on Windows CMD
Colors.disable_on_windows()

def print_status(message):
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {message}")

def print_success(message):
    print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {message}")

def print_warning(message):
    print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {message}")

def print_error(message):
    print(f"{Colors.RED}[ERROR]{Colors.NC} {message}")

def run_command(command, check=True, shell=False):
    """Run a command and return the result"""
    try:
        if platform.system() == "Windows":
            # On Windows, we need shell=True for most commands
            if isinstance(command, list):
                command = ' '.join(f'"{cmd}"' if ' ' in str(cmd) else str(cmd) for cmd in command)
            result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        else:
            result = subprocess.run(command, shell=shell, check=check, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr
    except FileNotFoundError:
        return False, "", "Command not found"

def check_python():
    """Check if Python is installed and meets requirements"""
    print_status("Checking Python installation...")
    
    python_cmd = "python" if platform.system() == "Windows" else "python3"
    success, stdout, stderr = run_command([python_cmd, "--version"])
    
    if not success:
        print_error("Python is not installed or not in PATH")
        if platform.system() == "Windows":
            print_error("Please install Python from https://python.org")
        else:
            print_error("Please install Python 3.8+ using your package manager")
        return False
    
    version = stdout.strip().split()[1]
    major, minor = map(int, version.split('.')[:2])
    
    if major < 3 or (major == 3 and minor < 8):
        print_error(f"Python {version} found, but Python 3.8+ is required")
        return False
    
    print_success(f"Python {version} found")
    return True

def check_tesseract():
    """Check if Tesseract is installed"""
    print_status("Checking Tesseract OCR...")
    
    success, stdout, stderr = run_command(["tesseract", "--version"])
    
    if not success:
        print_warning("Tesseract OCR not found")
        return False
    
    version_line = stdout.split('\n')[0]
    print_success(f"Tesseract found: {version_line}")
    
    # Check Arabic language support
    success, stdout, stderr = run_command(["tesseract", "--list-langs"])
    if success and "ara" in stdout:
        print_success("Arabic language support confirmed")
        return True
    else:
        print_warning("Arabic language pack not found")
        return False

def install_tesseract():
    """Install Tesseract based on the operating system"""
    system = platform.system()
    print_status(f"Installing Tesseract for {system}...")
    
    if system == "Windows":
        # Check for Chocolatey
        success, _, _ = run_command(["choco", "--version"])
        if success:
            print_status("Installing Tesseract via Chocolatey...")
            success, _, _ = run_command(["choco", "install", "tesseract", "-y"])
            if success:
                print_success("Tesseract installed via Chocolatey")
                return True
        
        print_warning("Chocolatey not found or installation failed")
        print_warning("Please install Tesseract manually:")
        print_warning("1. Download from: https://github.com/UB-Mannheim/tesseract/releases")
        print_warning("2. Install to default location")
        print_warning("3. Add to PATH environment variable")
        return False
        
    elif system == "Linux":
        # Try different package managers
        if os.path.exists("/usr/bin/apt"):
            print_status("Installing via apt (Ubuntu/Debian)...")
            commands = [
                ["sudo", "apt", "update"],
                ["sudo", "apt", "install", "-y", "tesseract-ocr", "tesseract-ocr-ara", "libtesseract-dev"]
            ]
        elif os.path.exists("/usr/bin/yum"):
            print_status("Installing via yum (CentOS/RHEL)...")
            commands = [
                ["sudo", "yum", "install", "-y", "tesseract", "tesseract-langpack-ara"]
            ]
        elif os.path.exists("/usr/bin/dnf"):
            print_status("Installing via dnf (Fedora)...")
            commands = [
                ["sudo", "dnf", "install", "-y", "tesseract", "tesseract-langpack-ara"]
            ]
        elif os.path.exists("/usr/bin/pacman"):
            print_status("Installing via pacman (Arch)...")
            commands = [
                ["sudo", "pacman", "-S", "--noconfirm", "tesseract", "tesseract-data-ara"]
            ]
        else:
            print_warning("Unknown Linux distribution")
            print_warning("Please install Tesseract manually using your package manager")
            return False
        
        for cmd in commands:
            success, _, stderr = run_command(cmd)
            if not success:
                print_error(f"Failed to run: {' '.join(cmd)}")
                print_error(stderr)
                return False
        
        print_success("Tesseract installed successfully")
        return True
        
    elif system == "Darwin":  # macOS
        success, _, _ = run_command(["brew", "--version"])
        if success:
            print_status("Installing via Homebrew...")
            success, _, _ = run_command(["brew", "install", "tesseract"])
            if success:
                print_success("Tesseract installed via Homebrew")
                return True
        
        print_warning("Homebrew not found")
        print_warning("Please install Homebrew first:")
        print_warning('curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh | bash')
        return False
    
    return False

def create_virtual_environment():
    """Create Python virtual environment"""
    print_status("Creating Python virtual environment...")
    
    venv_path = Path("venv")
    if venv_path.exists():
        print_warning("Virtual environment already exists")
        return True
    
    try:
        venv.create("venv", with_pip=True)
        print_success("Virtual environment created successfully")
        return True
    except Exception as e:
        print_error(f"Failed to create virtual environment: {e}")
        return False

def install_requirements():
    """Install Python requirements"""
    print_status("Installing Python requirements...")
    
    # Check for cross-platform requirements first, then fall back to regular requirements
    requirements_file = None
    if Path("requirements-cross-platform.txt").exists():
        requirements_file = "requirements-cross-platform.txt"
        print_status("Using cross-platform requirements file")
    elif Path("requirements.txt").exists():
        requirements_file = "requirements.txt"
        print_status("Using standard requirements file")
    else:
        print_error("No requirements file found!")
        return False
    
    system = platform.system()
    if system == "Windows":
        pip_cmd = ["venv\\Scripts\\pip.exe"]
    else:
        pip_cmd = ["venv/bin/pip"]
    
    # Upgrade pip first
    success, _, stderr = run_command(pip_cmd + ["install", "--upgrade", "pip"])
    if not success:
        print_warning(f"Failed to upgrade pip: {stderr}")
    
    # Install requirements
    success, stdout, stderr = run_command(pip_cmd + ["install", "-r", requirements_file])
    if not success:
        print_error(f"Failed to install requirements: {stderr}")
        if "pywin32" in stderr and system != "Windows":
            print_warning("Skipping Windows-specific packages on non-Windows system")
            # Try installing without pywin32 for non-Windows systems
            print_status("Attempting to install packages individually...")
            with open(requirements_file, 'r') as f:
                lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Skip Windows-specific packages on non-Windows
                    if system != "Windows" and any(pkg in line.lower() for pkg in ['pywin32', 'pyodbc']):
                        print_status(f"Skipping Windows-specific package: {line}")
                        continue
                    
                    package = line.split('==')[0].split('>=')[0].split('<=')[0]
                    success, _, stderr = run_command(pip_cmd + ["install", line])
                    if success:
                        print_success(f"Installed: {package}")
                    else:
                        print_warning(f"Failed to install {package}: {stderr}")
        else:
            return False
    
    print_success("Python requirements installed successfully")
    return True

def create_start_scripts():
    """Create platform-specific start scripts"""
    print_status("Creating start scripts...")
    
    system = platform.system()
    
    if system == "Windows":
        # Windows batch script
        with open("start_server.bat", "w") as f:
            f.write("@echo off\n")
            f.write("call venv\\Scripts\\activate.bat\n")
            f.write("python RestAPI.py\n")
            f.write("pause\n")
        print_success("Created start_server.bat")
    
    # Unix shell script (works on Linux and macOS)
    with open("start_server.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("source venv/bin/activate\n")
        f.write("python RestAPI.py\n")
    
    if system != "Windows":
        os.chmod("start_server.sh", 0o755)
        print_success("Created start_server.sh")

def main():
    """Main setup function"""
    print("=" * 50)
    print("Python Arabic OCR Server - Cross-Platform Setup")
    print("=" * 50)
    print()
    
    # Check Python
    if not check_python():
        sys.exit(1)
    
    # Check/Install Tesseract
    if not check_tesseract():
        print_warning("Tesseract not found. Attempting to install...")
        if not install_tesseract():
            print_warning("Tesseract installation failed. Please install manually.")
            print_warning("The server may not work properly without Tesseract.")
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Create start scripts
    create_start_scripts()
    
    print()
    print("=" * 50)
    print("Setup completed successfully!")
    print("=" * 50)
    print()
    print("To start the server:")
    
    system = platform.system()
    if system == "Windows":
        print("  start_server.bat")
        print()
        print("Or manually:")
        print("  venv\\Scripts\\activate.bat")
        print("  python RestAPI.py")
    else:
        print("  ./start_server.sh")
        print()
        print("Or manually:")
        print("  source venv/bin/activate")
        print("  python RestAPI.py")
    
    print()
    print("The server will be available at: http://127.0.0.1:5000")

if __name__ == "__main__":
    main()
