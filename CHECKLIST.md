# ✅ AEra Login – Funktions-Checklist

Vollständige Checkliste um sicherzustellen dass alles funktioniert.

---

## 🚀 Initialisierung

- [ ] Server läuft: `ps aux | grep uvicorn`
- [ ] Port 8000 erreichbar: `curl http://localhost:8000 | head -5`
- [ ] API antwortet: `curl http://localhost:8000/api/health`
- [ ] Datenbank existiert: `ls -la aera.db`
- [ ] Logs zeigen kein ERROR: `grep ERROR server.log`

---

## 🌐 Frontend (HTML/JS)

- [ ] **QR-Code sichtbar** – Im Browser sollte ein QR-Code auf der rechten Seite oder im "📱 QR-Code" Tab angezeigt werden
- [ ] **URL angezeigt** – Unter dem QR-Code sollte die URL stehen: `http://localhost:8000`
- [ ] **"📋 URL kopieren" Button funktioniert** – Klicken → "URL in Zwischenablage kopiert" Message
- [ ] **Debug Info sichtbar** – Unten sollte grauer Box mit Logs sein (F12 Console)
- [ ] **Tabs sichtbar** – "💻 Desktop" und "📱 QR-Code" Tabs sollten oben sein

---

## 🔗 Wallet-Verbindung (Desktop)

- [ ] **MetaMask installiert** – Chrome Extension oder Firefox Plugin
- [ ] **MetaMask entsperrt** – Password eingegeben, Wallet aktiv
- [ ] **"🔗 Wallet Verbinden" Button klickbar**
- [ ] **PopUp öffnet sich** – Nach Klick sollte MetaMask PopUp erscheinen
- [ ] **Genehmigung bestätigt** – "Genehmigen" klicken
- [ ] **Wallet-Adresse angezeigt** – Sollte so aussehen: `0x742d...6e0dE`
- [ ] **Netzwerk angezeigt** – Z.B. "sepolia" oder "ethereum"
- [ ] **Details-Box aktiv** – Grau Box mit Status, Wallet, Netzwerk, Score, Logins

---

## ✓ Verifizierung

- [ ] **"✓ Verifizieren & Score abrufen" Button sichtbar** – Nach Wallet-Verbindung
- [ ] **Button klickbar**
- [ ] **Loading Message** – "⏳ Verifizierung läuft..." angezeigt
- [ ] **Score angezeigt** – Z.B. "50/100" in einem Badge
- [ ] **Status aktualisiert** – "✅ Verifiziert"
- [ ] **Login Count aktualisiert** – Von "—" auf Zahl z.B. "1"
- [ ] **Success Message** – "✓ Verifizierung erfolgreich! Score: 50/100"

---

## 🔄 Mehrfach-Verifizierung

- [ ] **Score erhöht sich** – 2. Verifizierung → Score 51, 3. → Score 52, etc.
- [ ] **Login Count erhöht sich** – Von 1 → 2 → 3, etc.
- [ ] **Keine Errors** – Kein "error" in Console

---

## 📱 Mobile/QR-Tab

- [ ] **Tab "📱 QR-Code" klickbar**
- [ ] **Nach Klick:**
  - [ ] Desktop View verschwindet
  - [ ] QR-Code sichtbar (Canvas mit Quadraten/Pattern)
  - [ ] URL sichtbar unter QR-Code
  - [ ] "📋 URL in Zwischenablage kopieren" Button
  - [ ] Button funktioniert

---

## 🛠️ API-Endpoints

### Health Check
```bash
curl http://localhost:8000/api/health
# Sollte JSON mit status: "healthy" zurückgeben
```
- [ ] Status 200 OK
- [ ] Response: `{"status": "healthy", "service": "AEra Login v0.1", ...}`

### Verifizierung
```bash
curl -X POST http://localhost:8000/api/verify \
  -H "Content-Type: application/json" \
  -d '{"address":"0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE"}'
```
- [ ] Status 200 OK
- [ ] Response enthält: `is_human`, `address`, `resonance_score`, `login_count`
- [ ] `is_human: true`
- [ ] `resonance_score` ist integer zwischen 50-100

### User Daten
```bash
curl http://localhost:8000/api/user/0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE
```
- [ ] Status 200 OK
- [ ] Enthält Wallet-Daten

### Statistiken
```bash
curl http://localhost:8000/api/stats
```
- [ ] Status 200 OK
- [ ] Zeigt: `total_users`, `average_score`, `total_logins`

---

## 💾 Datenbank

### Überprüfe Datenbank-Einträge
```bash
sqlite3 aera.db
> SELECT COUNT(*) FROM users;
> SELECT * FROM users LIMIT 1;
> SELECT * FROM events LIMIT 5;
> .quit
```
- [ ] `users` Tabelle hat Einträge
- [ ] `events` Tabelle hat Einträge (login, signup)
- [ ] Score wird korrekt erhöht
- [ ] Timestamps sind gültig

---

## 🌐 Externe Erreichbarkeit (Optional)

### Lokal im Netzwerk
```bash
hostname -I  # z.B. 192.168.1.100
# Vom Smartphone: http://192.168.1.100:8000
```
- [ ] QR-Code sichtbar auf Smartphone
- [ ] URL angezeigt
- [ ] "URL kopieren" funktioniert

### Mit ngrok
```bash
ngrok http 8000
# URL: https://abc123def456.ngrok.io
```
- [ ] URL global erreichbar
- [ ] QR-Code funktioniert
- [ ] Link funktioniert
- [ ] Vom echten Smartphone testbar

---

## ⚠️ Error-Handling

- [ ] **MetaMask nicht installiert** → Error Message angezeigt: "MetaMask nicht gefunden..."
- [ ] **Wallet-Verbindung abgelehnt** → Error Message: "Wallet-Verbindung abgelehnt"
- [ ] **Server nicht erreichbar** → Error Message: "Verifizierungsfehler: ..."
- [ ] **Ungültige Wallet-Adresse** → Error Message vom Server
- [ ] **Browser Console hat keine RED Errors** – Nur Warnings/Info OK

---

## 🔐 Sicherheit

- [ ] **CORS aktiviert** – Requests von anderen Origins werden akzeptiert
- [ ] **CORS Origins konfiguriert** – `.env`: `CORS_ORIGINS=*` (für Development)
- [ ] **Keine Sensitive Daten in Logs** – Private Keys nicht geloggt
- [ ] **Datenbank verschlüsselt** (optional, für Production)

---

## 📊 Performance

- [ ] **Seite lädt < 2 Sekunden** – Zeitstempel bei Load im Console
- [ ] **QR-Code generiert sich schnell** – < 100ms
- [ ] **Verifizierung antwortet < 500ms** – Netzwerk-abhängig
- [ ] **Keine Memory Leaks** – Browser Memory stabil

---

## 📋 Browser-Kompatibilität

- [ ] **Chrome** – QR-Code sichtbar, MetaMask funktioniert
- [ ] **Firefox** – QR-Code sichtbar, MetaMask funktioniert
- [ ] **Safari (Mac)** – QR-Code sichtbar, MetaMask funktioniert
- [ ] **Safari (iOS)** – QR-Code sichtbar, URL kopierbar
- [ ] **Chrome (Android)** – QR-Code sichtbar, URL kopierbar

---

## 🎯 Endgültige Checkliste vor Production

- [ ] Alle oben Tests bestanden
- [ ] `.env` mit Production-URL gesetzt
- [ ] `.env` mit korrektem `CORS_ORIGINS` gesetzt
- [ ] HTTPS aktiviert (Let's Encrypt)
- [ ] Logs monitored (Sentry oder ähnlich)
- [ ] Datenbank-Backups konfiguriert
- [ ] Rate-Limiting aktiviert (optional)
- [ ] Docs aktualisiert mit finaler URL
- [ ] Testnutzer erstellt (manuelle Verifikation)
- [ ] Performance-Test bestanden (Last-Test mit ab oder k6)

---

## 🚀 Green Light?

Wenn alle Häkchen gesetzt sind → **Gehe zum nächsten Schritt!**

1. ✅ Alles lokal funktioniert
2. ✅ Im LAN erreichbar
3. ✅ Mit ngrok global erreichbar
4. ✅ Echte Wallets testen (TestNet!)
5. ✅ Production deployen

---

**Happy Launching! 🚀**
