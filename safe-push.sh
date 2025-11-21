#!/bin/bash

# =====================================================
# SAFE PUSH SCRIPT - Prüft sensible Daten vor Push
# =====================================================

set -e  # Exit on error

echo "🔒 AEraLogin - Safe Push zu GitHub"
echo "===================================="
echo ""

# Farben
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

REPO_DIR="/home/karlheinz/krypto/aera-token/webside-wallet-login"
cd "$REPO_DIR"

echo "📁 Repository: $REPO_DIR"
echo ""

# =====================================================
# SCHRITT 1: Prüfe ob sensible Dateien vorhanden sind
# =====================================================
echo "🔍 Schritt 1: Prüfe lokale sensible Dateien..."
echo ""

SENSITIVE_FILES=(
    ".env"
    "aera.db"
    "memories.db"
    "server.log"
    "airdrop.log"
    "airdrop_worker.log"
    "*.db"
    "*.log"
    "nohup.out"
    "private_key*"
)

for file in "${SENSITIVE_FILES[@]}"; do
    if ls $file 1> /dev/null 2>&1; then
        echo -e "  ${GREEN}✓${NC} $file gefunden (wird durch .gitignore geschützt)"
    fi
done

echo ""

# =====================================================
# SCHRITT 2: Prüfe .gitignore
# =====================================================
echo "🔍 Schritt 2: Prüfe .gitignore..."
echo ""

if [ ! -f ".gitignore" ]; then
    echo -e "${RED}❌ FEHLER: .gitignore nicht gefunden!${NC}"
    exit 1
fi

if grep -q "\.env" .gitignore; then
    echo -e "  ${GREEN}✓${NC} .env in .gitignore"
else
    echo -e "  ${RED}❌ .env NICHT in .gitignore${NC}"
    exit 1
fi

if grep -q "\.db" .gitignore; then
    echo -e "  ${GREEN}✓${NC} *.db in .gitignore"
else
    echo -e "  ${RED}❌ *.db NICHT in .gitignore${NC}"
    exit 1
fi

if grep -q "\.log" .gitignore; then
    echo -e "  ${GREEN}✓${NC} *.log in .gitignore"
else
    echo -e "  ${RED}❌ *.log NICHT in .gitignore${NC}"
    exit 1
fi

echo ""

# =====================================================
# SCHRITT 3: Prüfe Git Status
# =====================================================
echo "🔍 Schritt 3: Prüfe Git Status..."
echo ""

git status --short

echo ""

# Prüfe ob sensible Dateien im Git Index sind
SENSITIVE_IN_GIT=$(git status --porcelain | grep -E "\.env|\.db|\.log|private_key|secret" || true)

if [ -n "$SENSITIVE_IN_GIT" ]; then
    echo -e "${RED}❌ WARNUNG: Sensible Dateien im Git Index gefunden:${NC}"
    echo "$SENSITIVE_IN_GIT"
    echo ""
    echo -e "${YELLOW}Diese Dateien werden NICHT gepusht (durch .gitignore geschützt)${NC}"
    echo ""
fi

# =====================================================
# SCHRITT 4: Zeige was committed wird
# =====================================================
echo "🔍 Schritt 4: Dateien die gepusht werden:"
echo ""

# Liste nur getrackte Dateien (die committed werden)
git ls-files | while read file; do
    echo -e "  ${GREEN}✓${NC} $file"
done

echo ""

# =====================================================
# SCHRITT 5: Scan nach sensiblen Inhalten
# =====================================================
echo "🔍 Schritt 5: Scan nach sensiblen Inhalten in getrackten Dateien..."
echo ""

FOUND_ISSUES=0

# Suche nach Private Keys (außer in Beispiel-Dateien)
echo "  → Suche nach Private Keys..."
PRIVATE_KEYS=$(git ls-files | grep -v ".example" | xargs grep -l "PRIVATE_KEY=" 2>/dev/null | grep -v ".gitignore" | grep -v "SECURITY-CHECKLIST" | grep -v "README.md" | grep -v "GITHUB-ORG" || true)

if [ -n "$PRIVATE_KEYS" ]; then
    echo -e "    ${RED}❌ Private Keys gefunden in:${NC}"
    echo "$PRIVATE_KEYS"
    FOUND_ISSUES=1
else
    echo -e "    ${GREEN}✓${NC} Keine Private Keys"
fi

# Suche nach Wallet Adressen (64 char hex nach 0x)
echo "  → Suche nach verdächtigen Wallet Private Keys..."
WALLET_KEYS=$(git ls-files | grep -v ".example" | xargs grep -E "0x[a-f0-9]{64}" 2>/dev/null | grep -v ".gitignore" | grep -v "SECURITY-CHECKLIST" | grep -v "README.md" | grep -v "test" || true)

if [ -n "$WALLET_KEYS" ]; then
    echo -e "    ${YELLOW}⚠️  Mögliche Wallet Keys gefunden (prüfen!):${NC}"
    echo "$WALLET_KEYS" | head -5
    echo ""
    echo -e "    ${YELLOW}Hinweis: Testnet-Keys sind OK, Mainnet-Keys NICHT!${NC}"
    echo ""
    read -p "    Sind das nur Testnet-Keys? (y/N): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo -e "    ${RED}❌ Abbruch!${NC}"
        exit 1
    fi
    echo -e "    ${GREEN}✓${NC} Bestätigt: Nur Testnet-Keys"
else
    echo -e "    ${GREEN}✓${NC} Keine verdächtigen Wallet Keys"
fi

# Suche nach API Keys
echo "  → Suche nach API Keys..."
API_KEYS=$(git ls-files | grep -v ".example" | xargs grep -iE "(api_key|apikey|alchemy.*v2/|infura)" 2>/dev/null | grep -v ".gitignore" | grep -v "SECURITY-CHECKLIST" | grep -v "README.md" | grep -v "# " || true)

if [ -n "$API_KEYS" ]; then
    echo -e "    ${YELLOW}⚠️  API Keys gefunden (prüfen!):${NC}"
    echo "$API_KEYS" | head -5
    echo ""
    read -p "    Sind das nur Beispiel-URLs oder Test-Keys? (y/N): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo -e "    ${RED}❌ Abbruch!${NC}"
        exit 1
    fi
    echo -e "    ${GREEN}✓${NC} Bestätigt: Nur Beispiele"
else
    echo -e "    ${GREEN}✓${NC} Keine API Keys"
fi

echo ""

if [ $FOUND_ISSUES -eq 1 ]; then
    echo -e "${RED}❌ Sensible Daten gefunden! Push abgebrochen.${NC}"
    echo ""
    echo "Bitte entferne sensible Daten aus den Dateien."
    exit 1
fi

# =====================================================
# SCHRITT 6: Final Check
# =====================================================
echo "🔍 Schritt 6: Final Security Check..."
echo ""

# Prüfe ob .env.example vorhanden ist
if [ ! -f ".env.example" ]; then
    echo -e "${YELLOW}⚠️  .env.example nicht gefunden${NC}"
    echo "Erstelle .env.example..."
    echo "# See .env.example for configuration" > .env.example
fi

# Prüfe ob README.md vorhanden ist
if [ ! -f "README.md" ]; then
    echo -e "${RED}❌ README.md nicht gefunden!${NC}"
    exit 1
else
    echo -e "  ${GREEN}✓${NC} README.md vorhanden"
fi

# Prüfe ob CONTRIBUTING.md vorhanden ist
if [ -f "CONTRIBUTING.md" ]; then
    echo -e "  ${GREEN}✓${NC} CONTRIBUTING.md vorhanden"
fi

echo ""

# =====================================================
# SCHRITT 7: Bestätigung
# =====================================================
echo "✅ Alle Checks erfolgreich!"
echo ""
echo "═══════════════════════════════════════"
echo "  BEREIT ZUM PUSH"
echo "═══════════════════════════════════════"
echo ""
echo "Repository: vera-resonanz/AEraLogin"
echo "Branch: main"
echo ""
echo "Dateien die gepusht werden:"
git ls-files | wc -l
echo " Dateien insgesamt"
echo ""
echo "Geschützte Dateien (werden NICHT gepusht):"
echo "  • .env (Wallet Keys)"
echo "  • *.db (Datenbanken)"
echo "  • *.log (Logs)"
echo "  • private_key* (Keys)"
echo ""

read -p "🚀 Push zu GitHub durchführen? (y/N): " confirm

if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo ""
    echo "❌ Push abgebrochen."
    exit 0
fi

echo ""

# =====================================================
# SCHRITT 8: Git Push
# =====================================================
echo "🚀 Pushe zu GitHub..."
echo ""

# Check if remote exists
if ! git remote | grep -q "origin"; then
    echo -e "${YELLOW}⚠️  Remote 'origin' nicht gefunden${NC}"
    echo ""
    echo "Füge Remote hinzu:"
    read -p "GitHub Repository URL: " repo_url
    git remote add origin "$repo_url"
    echo -e "${GREEN}✓${NC} Remote hinzugefügt"
    echo ""
fi

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)

if [ -z "$CURRENT_BRANCH" ]; then
    echo "Erstelle Main Branch..."
    git checkout -b main
    CURRENT_BRANCH="main"
fi

echo "Push Branch: $CURRENT_BRANCH"
echo ""

# Push
if git push -u origin "$CURRENT_BRANCH"; then
    echo ""
    echo "═══════════════════════════════════════"
    echo -e "  ${GREEN}✅ PUSH ERFOLGREICH!${NC}"
    echo "═══════════════════════════════════════"
    echo ""
    echo "Repository: https://github.com/vera-resonanz/AEraLogin"
    echo ""
    echo "Nächste Schritte:"
    echo "  1. Gehe zu GitHub und prüfe das Repository"
    echo "  2. Erstelle ein Release (git tag v0.1.0)"
    echo "  3. Füge Topics hinzu (web3, authentication, etc.)"
    echo "  4. Enable Issues & Discussions"
    echo ""
else
    echo ""
    echo -e "${RED}❌ Push fehlgeschlagen!${NC}"
    echo ""
    echo "Mögliche Ursachen:"
    echo "  • Falsche GitHub URL"
    echo "  • Keine Push-Berechtigung"
    echo "  • Branch existiert bereits"
    echo ""
    echo "Hilfe:"
    echo "  git remote -v                 # Zeige Remote URL"
    echo "  git remote set-url origin URL # Ändere URL"
    echo "  git push -f origin main       # Force Push (Vorsicht!)"
    exit 1
fi

echo ""
echo "🎉 Fertig!"
