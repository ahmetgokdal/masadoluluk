@echo off
cls
echo.
echo Smart Cabin Monitoring System
echo ==============================
echo.
echo Starting application...
echo.

python smart_cabin_desktop.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to start!
    echo.
    echo Solutions:
    echo 1. Install Python 3.8+ from python.org
    echo 2. Install Node.js 14+ from nodejs.org
    echo 3. Check KURULUM_REHBERI.md
    echo.
    pause
)
