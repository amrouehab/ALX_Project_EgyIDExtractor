@echo off
echo Setting up Python Arabic OCR Server...
echo.

echo Creating virtual environment...
python -m venv .

echo Activating virtual environment...
call Scripts\activate.bat

echo Installing required packages...
pip install -r requirements.txt

echo.
echo Setup complete! You can now run start_server.bat to start the server.
pause
