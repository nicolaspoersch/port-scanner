@echo off

echo Warning: To run this program, you need Python, Pip, Colorama, whois, tabulate, and Requests.
echo If you want to run with color, install colorama, whois, tabulate, and requests with this installer, follow the checks/instructions below:
echo Checking Python installation...

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python not found. Please download and install Python from: https://www.python.org/downloads/
    goto :exit
)

echo Python found.

:: Check if pip is installed
where pip >nul 2>nul
if %errorlevel% neq 0 (
    echo Pip not found. Please make sure pip is installed and available in the system PATH.
    echo You can download and install pip from: https://pip.pypa.io/en/stable/installation/ or move the get-pip.py in this folder to the python directory.
    echo After installing pip, make sure to add the pip installation directory to the system PATH.
    echo If you're unsure how to do this, you can follow the instructions here: https://www.geeksforgeeks.org/how-to-install-pip-on-windows/
    echo Tip: You can open a CMD window in the Python installation folder by typing “cmd” in the file explorer address/path to run python get-pip.py.
    goto :exit
)

echo Pip found.

echo Installing whois...
:: Install whois
pip install whois
echo Whois installed successfully!

echo Installing tabulate...
:: Install tabulate
pip install tabulate
echo Tabulate installed successfully!

:exit
pause
