@echo off
chcp 65001 >nul
title PharmaCon POS - App Server

set PYTHON_CMD=python
set PORT=5000
set HOST=127.0.0.1
set FLASK_APP=app.py
set FLASK_ENV=development

echo ==========================================
echo   PharmaCon POS - Direct App Launch
echo ==========================================
echo.

REM Check Python availability
echo [INFO] Checking Python installation...
%PYTHON_CMD% --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found in PATH.
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)
for /f "tokens=2" %%a in ('%PYTHON_CMD% --version') do set PY_VER=%%a
echo [OK] Python %PY_VER% detected.

REM Check/activate virtual environment
if exist "venv\Scripts\activate.bat" (
    echo [INFO] Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [WARNING] No virtual environment found at .\venv
    echo [INFO] Using system Python.
    echo.
)

REM Install/update dependencies
if exist "requirements.txt" (
    echo [INFO] Checking dependencies...
    %PYTHON_CMD% -m pip show flask >nul 2>&1
    if errorlevel 1 (
        echo [INFO] Installing dependencies from requirements.txt...
        %PYTHON_CMD% -m pip install -r requirements.txt --quiet
        if errorlevel 1 (
            echo [ERROR] Failed to install dependencies.
            pause
            exit /b 1
        )
        echo [OK] Dependencies installed.
    ) else (
        echo [OK] Dependencies satisfied.
    )
) else (
    echo [WARNING] requirements.txt not found, skipping dependency check.
)

REM Initialize database if needed
if not exist "pharmacon.db" (
    echo [INFO] Initializing database...
    %PYTHON_CMD% -c "from database_sqlite import init_db; init_db()"
    if errorlevel 1 (
        echo [ERROR] Database initialization failed.
        pause
        exit /b 1
    )
    echo [OK] Database initialized.
) else (
    echo [OK] Database exists.
)

echo.
echo [INFO] Starting PharmaCon POS on http://%HOST%:%PORT%
echo [INFO] Default admin login: admin / admin123
echo [INFO] Press Ctrl+C to stop the server
echo ==========================================
echo.

REM Start Flask server directly (foreground)
set FLASK_RUN_HOST=%HOST%
set FLASK_RUN_PORT=%PORT%
%PYTHON_CMD% %FLASK_APP%

echo.
echo [INFO] Server stopped.
echo ==========================================
pause