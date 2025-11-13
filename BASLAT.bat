@echo off
title Smart Cabin Monitoring - Starting...

echo.
echo ====================================================
echo     SMART CABIN MONITORING SYSTEM
echo ====================================================
echo.
echo Starting system...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    echo.
    echo Python 3.8 or higher required.
    echo Download from: https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found!
    echo.
    echo Node.js 14 or higher required.
    echo Download from: https://nodejs.org/
    echo.
    pause
    exit /b 1
)

echo [OK] Requirements checked
echo.

REM Start the application
python smart_cabin_desktop.py

REM Wait on error
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] An error occurred!
    echo.
    echo Check KURULUM_REHBERI.md for help
    pause
)

exit /b 0
