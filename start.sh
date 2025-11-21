#!/bin/bash

# AEra Login Quick Start Script
# Startet den Server mit automatischer Dependency-Installation

set -e

echo "🚀 AEra Login Server – Quick Start"
echo "=================================="
echo ""

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Python-Version prüfen
echo "${BLUE}Prüfe Python-Version...${NC}"
python --version || { echo "${RED}Python nicht gefunden!${NC}"; exit 1; }

# Virtuelle Umgebung (optional aber empfohlen)
if [ ! -d "venv" ]; then
    echo "${YELLOW}Erstelle virtuelle Umgebung...${NC}"
    python -m venv venv
    echo "${GREEN}✓ Virtuelle Umgebung erstellt${NC}"
fi

# Aktiviere venv
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "${GREEN}✓ Virtuelle Umgebung aktiviert${NC}"
echo ""

# Dependencies installieren
echo "${BLUE}Installiere Dependencies...${NC}"
pip install --upgrade pip > /dev/null
pip install -r requirements.txt > /dev/null
echo "${GREEN}✓ Dependencies installiert${NC}"
echo ""

# Starte Server
echo "${BLUE}Starte AEra Login Server...${NC}"
echo "${YELLOW}URL: http://localhost:8000${NC}"
echo "${YELLOW}Zum Beenden: Ctrl+C${NC}"
echo ""

uvicorn server:app --reload --port 8000
