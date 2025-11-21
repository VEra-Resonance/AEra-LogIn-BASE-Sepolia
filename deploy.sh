#!/bin/bash
#
# AEra Login Server - Deployment Script
# Startet Server korrekt mit venv und eth_account support
#

set -e

cd "$(dirname "$0")"

VENV_PATH="./venv"
DB_FILE="./aera.db"
LOG_DIR="./logs"
SERVER_PID_FILE=".server.pid"

echo "=================================================="
echo "  AEra Login Server - Deployment"
echo "=================================================="

# ===== ÜBERPRÜFE VENV =====
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ Virtual Environment nicht gefunden: $VENV_PATH"
    echo ""
    echo "Bitte erst einrichten mit:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

echo "✓ Virtual Environment gefunden"

# ===== ÜBERPRÜFE LOG-VERZEICHNIS =====
if [ ! -d "$LOG_DIR" ]; then
    echo "📁 Erstelle logs-Verzeichnis..."
    mkdir -p "$LOG_DIR"
fi

echo "✓ Logs-Verzeichnis: $LOG_DIR"

# ===== ÜBERPRÜFE ABHÄNGIGKEITEN =====
echo ""
echo "Überprüfe Python-Abhängigkeiten..."

source "$VENV_PATH/bin/activate"

# Überprüfe eth_account
python3 -c "from eth_account import Account; print('✓ eth_account verfügbar')" || {
    echo "❌ eth_account NICHT verfügbar - installiere..."
    pip install eth-account
}

# Überprüfe weitere kritische Pakete
python3 -c "from web3 import Web3; print('✓ web3 verfügbar')" || {
    echo "❌ web3 NICHT verfügbar"
    exit 1
}

python3 -c "from fastapi import FastAPI; print('✓ fastapi verfügbar')" || {
    echo "❌ fastapi NICHT verfügbar"
    exit 1
}

# ===== KILL ALTEN PROZESS =====
if [ -f "$SERVER_PID_FILE" ]; then
    OLD_PID=$(cat "$SERVER_PID_FILE")
    if kill -0 "$OLD_PID" 2>/dev/null; then
        echo "Stoppe alten Server (PID: $OLD_PID)..."
        kill "$OLD_PID" || true
        sleep 1
    fi
fi

# Alternativ: pkill
pkill -f "python3 server.py" || true
sleep 1

# ===== STARTE SERVER =====
echo ""
echo "=================================================="
echo "🚀 Starte AEra Login Server..."
echo "=================================================="

python3 server.py > server.log 2>&1 &
SERVER_PID=$!

echo $SERVER_PID > "$SERVER_PID_FILE"

echo "✓ Server gestartet (PID: $SERVER_PID)"
echo ""
echo "=================================================="
echo "  📋 DEPLOYMENT FERTIG"
echo "=================================================="
echo ""
echo "  🌐 Öffne: http://localhost:8820"
echo "  🔗 Remote:  http://192.168.178.50:8820"
echo "  📊 Logs:    tail -f server.log"
echo "  📈 Activity: tail -f logs/activity.log"
echo ""
echo "  🔐 SICHERHEIT:"
echo "     ✓ Signatur-Verifikation AKTIV"
echo "     ✓ MetaMask-Validierung ERZWUNGEN"
echo "     ✓ Nur ECHTE MetaMask-Signaturen akzeptiert"
echo ""
echo "=================================================="
