#!/bin/bash

# Renk kodları
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║     🏢  AKILLI KABİN İZLEME SİSTEMİ                         ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 Sistem başlatılıyor..."
echo ""

# Python kontrol
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 bulunamadı!${NC}"
    echo ""
    echo "Python 3.8 veya üzeri gerekli."
    echo "Kurulum: sudo apt install python3 python3-pip"
    exit 1
fi

# Node.js kontrol
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js bulunamadı!${NC}"
    echo ""
    echo "Node.js 14 veya üzeri gerekli."
    echo "Kurulum: https://nodejs.org/"
    exit 1
fi

echo -e "${GREEN}✅ Gereksinimler kontrol edildi${NC}"
echo ""

# Ana uygulamayı başlat
python3 smart_cabin_desktop.py

# Hata durumunda
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ Bir hata oluştu!${NC}"
    read -p "Çıkmak için Enter'a basın..."
    exit 1
fi
