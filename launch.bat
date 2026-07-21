@echo off
setlocal

title PharmaCon POS Launcher

set "XAMPP_DIR=C:\xampp"
set "MYSQL_BAT=%XAMPP_DIR%\mysql_start.bat"
set "APACHE_BAT=%XAMPP_DIR%\apache_start.bat"

echo ========================================
echo   PharmaCon POS Launcher
echo ========================================
echo.

if not exist "%MYSQL_BAT%" (
    echo [ERROR] XAMPP not found at %XAMPP_DIR%
    echo Install XAMPP or edit this script to set the correct path.
    pause
    exit /b 1
)

echo [...] Checking MySQL...
netstat -ano | findstr ":3306.*LISTENING" >nul
if errorlevel 1 (
    echo [...] Starting MySQL...
    start "" "%MYSQL_BAT%"
    ping -n 6 127.0.0.1 >nul
) else (
    echo [OK] MySQL is already running.
)

echo.
echo [...] Checking Apache...
netstat -ano | findstr ":80.*LISTENING" >nul
if errorlevel 1 (
    echo [...] Starting Apache...
    start "" "%APACHE_BAT%"
    ping -n 6 127.0.0.1 >nul
) else (
    echo [OK] Apache is already running.
)

cd /d "%~dp0"

set "PYTHON_EXE="
if exist "venv\Scripts\python.exe" (
    set "PYTHON_EXE=venv\Scripts\python.exe"
) else (
    set "PYTHON_EXE=python"
)

echo.
echo [...] Starting PharmaCon POS...
echo Close the application window to stop the server.
echo.

start "" "%PYTHON_EXE%" app.py

ping -n 7 127.0.0.1 >nul

echo [...] Opening browser...
start http://localhost:5000

echo.
echo ========================================
echo   PharmaCon POS is running.
echo   Close this window to exit the launcher.
echo ========================================
echo.

pause
