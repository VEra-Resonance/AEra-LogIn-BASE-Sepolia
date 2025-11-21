#!/bin/bash

# =====================================================
# GIT HISTORY CLEANUP - .env entfernen
# =====================================================
#
# WARNUNG: Dies ändert die Git-History!
# Nur ausführen wenn Sie sicher sind!
#
# =====================================================

echo "🚨 Git History Cleanup für .env"
echo "================================"
echo ""
echo "⚠️  WARNUNG: Dies wird die Git-History ändern!"
echo "⚠️  Alle Commits die .env enthalten werden modifiziert!"
echo ""
echo "Backup erstellen..."

# Backup erstellen
BACKUP_DIR="/home/karlheinz/krypto/aera-token/webside-wallet-login-backup-$(date +%Y%m%d-%H%M%S)"
cp -r /home/karlheinz/krypto/aera-token/webside-wallet-login "$BACKUP_DIR"
echo "✅ Backup erstellt: $BACKUP_DIR"
echo ""

cd /home/karlheinz/krypto/aera-token/webside-wallet-login

echo "Schritt 1: Entferne .env aus Git Index..."
git rm --cached .env 2>/dev/null || echo "  → .env nicht im Index"

echo ""
echo "Schritt 2: BFG Repo-Cleaner verwenden (empfohlen)"
echo "=================================================="
echo ""
echo "Option A: BFG installieren und verwenden (EINFACH)"
echo "--------------------------------------------------"
echo "# Ubuntu/Debian:"
echo "sudo apt install bfg"
echo ""
echo "# Dann ausführen:"
echo "cd /home/karlheinz/krypto/aera-token/webside-wallet-login"
echo "bfg --delete-files .env"
echo "git reflog expire --expire=now --all"
echo "git gc --prune=now --aggressive"
echo ""
echo ""
echo "Option B: git filter-branch (KOMPLIZIERT)"
echo "------------------------------------------"
echo "git filter-branch --force --index-filter \\"
echo "  'git rm --cached --ignore-unmatch .env' \\"
echo "  --prune-empty --tag-name-filter cat -- --all"
echo ""
echo "git reflog expire --expire=now --all"
echo "git gc --prune=now --aggressive"
echo ""
echo ""
echo "Schritt 3: Force Push (falls Remote existiert)"
echo "==============================================="
echo "⚠️  NUR wenn Sie sicher sind:"
echo "git push origin --force --all"
echo "git push origin --force --tags"
echo ""
echo ""
echo "🔒 WICHTIG NACH CLEANUP:"
echo "========================"
echo "1. ✅ Neue Wallet erstellen"
echo "2. ✅ Alte Wallet Funds transferieren"
echo "3. ✅ .env mit neuen Keys aktualisieren"
echo "4. ✅ Alte Private Keys NIEMALS wieder nutzen"
echo ""
echo "Backup Location: $BACKUP_DIR"
