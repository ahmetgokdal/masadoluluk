@echo off
echo.
echo Node.js Test
echo ============
echo.

echo Checking Node.js...
node --version
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found!
    pause
    exit /b 1
)

echo.
echo Checking npm...
npm --version
if %errorlevel% neq 0 (
    echo [ERROR] npm not found!
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Node.js and npm are installed!
echo.
pause
