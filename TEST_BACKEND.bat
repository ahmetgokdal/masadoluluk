@echo off
echo.
echo Backend Test
echo ============
echo.

cd backend

echo Setting environment...
set MONGO_URL=mongita:///C:/test/cabin_db
set DB_NAME=smart_cabin_db
set CORS_ORIGINS=*

echo.
echo Testing Python imports...
python -c "import server; print('[OK] server.py can be imported')"

if %errorlevel% neq 0 (
    echo [ERROR] server.py import failed!
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Backend imports work!
echo.
pause
