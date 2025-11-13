@echo off
chcp 65001 >nul
title Akıllı Kabin İzleme Sistemi - Başlatılıyor...

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║     🏢  AKILLI KABİN İZLEME SİSTEMİ                         ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🚀 Sistem başlatılıyor...
echo.

REM Python kurulu mu kontrol et
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python bulunamadı!
    echo.
    echo Python 3.8 veya üzeri gerekli.
    echo https://www.python.org/downloads/ adresinden indirin.
    echo.
    pause
    exit /b 1
)

REM Node.js kurulu mu kontrol et
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js bulunamadı!
    echo.
    echo Node.js 14 veya üzeri gerekli.
    echo https://nodejs.org/ adresinden indirin.
    echo.
    pause
    exit /b 1
)

echo ✅ Gereksinimler kontrol edildi
echo.

REM Ana uygulamayı başlat
python smart_cabin_desktop.py

REM Hata durumunda bekle
if %errorlevel% neq 0 (
    echo.
    echo ❌ Bir hata oluştu!
    pause
)

exit /b 0
