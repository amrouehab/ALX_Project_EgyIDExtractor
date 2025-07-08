#!/usr/bin/env python3
"""
Final Setup Verification and User Guide
This script provides a comprehensive overview of the setup status and next steps
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color
    
    @staticmethod
    def disable_on_windows():
        if platform.system() == "Windows":
            for attr in dir(Colors):
                if not attr.startswith('_') and attr != 'disable_on_windows':
                    setattr(Colors, attr, "")

Colors.disable_on_windows()

def print_header(title):
    print(f"\n{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{title:^60}{Colors.NC}")
    print(f"{Colors.CYAN}{'='*60}{Colors.NC}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.NC}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.NC}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.NC}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.NC}")

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception:
        return False, "", ""

def check_file_exists(filepath, description):
    if Path(filepath).exists():
        print_success(f"{description}: {filepath}")
        return True
    else:
        print_error(f"{description} not found: {filepath}")
        return False

def main():
    print_header("PYTHON ARABIC OCR SERVER - SETUP STATUS")
    
    print(f"\n{Colors.BOLD}Project Status Report{Colors.NC}")
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Directory: {os.getcwd()}")
    
    # Check core files
    print_header("CORE PROJECT FILES")
    
    core_files = [
        ("RestAPI.py", "Main Flask Application"),
        ("requirements.txt", "Python Dependencies"),
        ("setup.py", "Cross-Platform Setup Script"),
        ("README.md", "Project Documentation"),
        ("INSTALLATION.md", "Installation Guide")
    ]
    
    files_ok = 0
    for file, desc in core_files:
        if check_file_exists(file, desc):
            files_ok += 1
    
    # Check setup files
    print_header("SETUP SCRIPTS")
    
    setup_files = [
        ("setup.bat", "Windows Setup Script"),
        ("setup.sh", "Linux/macOS Setup Script"), 
        ("start_server.bat", "Windows Server Start"),
        ("start_server.sh", "Linux/macOS Server Start"),
        ("test_setup.bat", "Windows Test Script"),
        ("test_setup.sh", "Linux/macOS Test Script")
    ]
    
    setup_ok = 0
    for file, desc in setup_files:
        if check_file_exists(file, desc):
            setup_ok += 1
    
    # Check virtual environment
    print_header("VIRTUAL ENVIRONMENT")
    
    venv_exists = Path("venv").exists()
    if venv_exists:
        print_success("Virtual environment directory exists")
        
        # Check virtual environment structure
        system = platform.system()
        if system == "Windows":
            python_exe = Path("venv/Scripts/python.exe")
            pip_exe = Path("venv/Scripts/pip.exe")
            activate_script = Path("venv/Scripts/activate.bat")
        else:
            python_exe = Path("venv/bin/python")
            pip_exe = Path("venv/bin/pip")
            activate_script = Path("venv/bin/activate")
        
        venv_ok = 0
        if python_exe.exists():
            print_success("Python executable found in virtual environment")
            venv_ok += 1
        else:
            print_error("Python executable not found in virtual environment")
        
        if pip_exe.exists():
            print_success("Pip executable found in virtual environment")
            venv_ok += 1
        else:
            print_error("Pip executable not found in virtual environment")
            
        if activate_script.exists():
            print_success("Activation script found")
            venv_ok += 1
        else:
            print_error("Activation script not found")
    else:
        print_error("Virtual environment not found")
        venv_ok = 0
    
    # Check Tesseract
    print_header("TESSERACT OCR")
    
    tesseract_ok = 0
    success, stdout, stderr = run_command("tesseract --version")
    if success:
        version = stdout.split('\n')[0] if stdout else "Unknown version"
        print_success(f"Tesseract found: {version}")
        tesseract_ok += 1
        
        # Check Arabic support
        success, stdout, stderr = run_command("tesseract --list-langs")
        if success and "ara" in stdout:
            print_success("Arabic language support confirmed")
            tesseract_ok += 1
        else:
            print_warning("Arabic language support not found")
    else:
        print_error("Tesseract not found in PATH")
    
    # Summary
    print_header("SETUP SUMMARY")
    
    total_score = files_ok + setup_ok + (3 if venv_exists and venv_ok == 3 else 0) + tesseract_ok
    max_score = len(core_files) + len(setup_files) + 3 + 2  # 3 for venv, 2 for tesseract
    
    percentage = (total_score / max_score) * 100
    
    print(f"\n{Colors.BOLD}Overall Setup Score: {total_score}/{max_score} ({percentage:.1f}%){Colors.NC}")
    
    if percentage >= 90:
        print_success("🎉 EXCELLENT! Your setup is complete and ready to use!")
        setup_status = "READY"
    elif percentage >= 70:
        print_warning("⚡ GOOD! Your setup is mostly complete with minor issues.")
        setup_status = "MOSTLY_READY"
    else:
        print_error("🔧 INCOMPLETE! Your setup needs attention.")
        setup_status = "NEEDS_WORK"
    
    # Provide next steps
    print_header("NEXT STEPS")
    
    if setup_status == "READY":
        print_info("Your Python Arabic OCR Server is ready to use!")
        print()
        print(f"{Colors.BOLD}To start the server:{Colors.NC}")
        if platform.system() == "Windows":
            print("  start_server.bat")
        else:
            print("  ./start_server.sh")
        print()
        print("Or manually:")
        if platform.system() == "Windows":
            print("  venv\\Scripts\\activate.bat")
        else:
            print("  source venv/bin/activate")
        print("  python RestAPI.py")
        print()
        print(f"{Colors.BOLD}Server will be available at:{Colors.NC}")
        print("  🌐 http://127.0.0.1:5000")
        
    elif setup_status == "MOSTLY_READY":
        print_info("Run setup again to fix remaining issues:")
        print("  python setup.py")
        print()
        print("Or check the installation guide:")
        print("  📖 INSTALLATION.md")
        
    else:
        print_info("Setup is incomplete. Please run:")
        print("  python setup.py")
        print()
        print("If setup fails, check:")
        print("  📖 INSTALLATION.md (detailed troubleshooting)")
        print("  🛠️  Manual setup instructions")
    
    # Additional resources
    print_header("RESOURCES")
    
    print(f"{Colors.BOLD}📁 Project Files:{Colors.NC}")
    print("  • RestAPI.py - Main Flask application")
    print("  • setup.py - Cross-platform setup script") 
    print("  • INSTALLATION.md - Detailed installation guide")
    print("  • README.md - Project overview")
    
    print(f"\n{Colors.BOLD}🧪 Testing:{Colors.NC}")
    if platform.system() == "Windows":
        print("  • test_setup.bat - Verify installation")
    else:
        print("  • ./test_setup.sh - Verify installation")
    
    print(f"\n{Colors.BOLD}🆘 Need Help?{Colors.NC}")
    print("  1. Check INSTALLATION.md for troubleshooting")
    print("  2. Run test scripts to identify issues")
    print("  3. Verify Python 3.8+ and Tesseract are installed")
    print("  4. Check GitHub issues for known problems")
    
    print(f"\n{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.GREEN}Happy coding with Python Arabic OCR Server! 🚀{Colors.NC}")
    print(f"{Colors.CYAN}{'='*60}{Colors.NC}")
    
    return setup_status == "READY"

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
