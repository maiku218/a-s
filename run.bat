@echo off
chcp 65001 >nul
title PharmaCon POS - SQLite Edition

echo ==========================================
echo   PharmaCon POS - SQLite Edition
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo [INFO] Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [WARNING] No virtual environment found.
    echo Using system Python instead.
    echo.
    echo To create a virtual environment, run:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
)

REM Install dependencies if needed
echo [INFO] Checking dependencies...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing dependencies from requirements.txt...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b 1
    )
)

REM Initialize database if it doesn't exist
if not exist "pharmacon.db" (
    echo [INFO] Initializing SQLite database...
    python -c "from database_sqlite import init_db; init_db()"
    echo [INFO] Database initialized successfully!
) else (
    echo [INFO] Database already exists.
)

REM Start Flask server in background and open browser
echo.
echo [INFO] Starting PharmaCon POS server...
echo [INFO] Default login: admin / admin123
echo.

REM Start Flask in background
start /B python app.py > server.log 2>&1

REM Wait for server to start
echo [INFO] Waiting for server to start...
timeout /t 2 /nobreak >nul

REM Open browser
echo [INFO] Opening browser to http://localhost:5000
start http://localhost:5000

echo.
echo [INFO] Server is running in background.
echo [INFO] Check server.log for output.
echo [INFO] Close this window when done.
echo ==========================================
echo.

REM Keep window open
pause
