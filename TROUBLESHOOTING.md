# 🔧 AEra Login – Troubleshooting Guide

Lösungen für häufige Probleme.

---

## ❌ Problem: Webseite öffnet sich nicht

### Symptom
- Browser zeigt "Die Seite konnte nicht geöffnet werden"
- oder "Connection refused"

### Lösung

**Schritt 1: Prüfe ob Server läuft**
```bash
ps aux | grep uvicorn | grep -v grep
```

Falls nichts angezeigt wird → Server läuft nicht!

**Schritt 2: Server starten**
```bash
cd /home/karlheinz/krypto/aera-token/webside-wallet-login
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

**Schritt 3: Teste mit curl**
```bash
curl http://localhost:8000
```

Sollte HTML zurückgeben (nicht Error).

**Schritt 4: Browser URL richtig?**
- ✅ Richtig: `http://localhost:8000`
- ❌ Falsch: `http://localhost:8000/index.html`
- ❌ Falsch: `localhost:8000` (ohne http://)
- ❌ Falsch: `http://localhost:3000` (falscher Port)

---

## ❌ Problem: QR-Code nicht sichtbar

### Symptom
- Webseite lädt
- Aber QR-Code ist leer
- Oder nur Text sichtbar

### Lösung

**Schritt 1: Browser Console öffnen**
```
F12 → Console (unten)
```

**Schritt 2: Sollte Logs zeigen:**
```
[AEra] === AEra Login gestartet ===
[AEra] URL: http://localhost:8000/
[AEra] QR-Code generiert für: http://localhost:8000/
```

Falls nicht → JavaScript lädt nicht!

**Schritt 3: Seite neu laden**
```
Ctrl+R  (Windows/Linux)
Cmd+R   (Mac)
```

**Schritt 4: Cache leeren**
```
Ctrl+Shift+Delete → Cookies & Cache löschen
```

**Schritt 5: Ganz neuer Browser-Tab**
```
Ctrl+T → http://localhost:8000 eingeben
```

---

## ❌ Problem: URL wird nicht angezeigt

### Symptom
- QR-Code sichtbar aber leer
- URL Box zeigt "loading..."
- Oder "—"

### Lösung

Wahrscheinlich CSS-Problem. Versuche:

```javascript
// Browser Console (F12) eingeben:
console.log('PUBLIC_URL:', window.location.href);
document.getElementById('urlDisplay').textContent = window.location.href;
```

Falls das funktioniert → CSS/Layout-Bug.

---

## ❌ Problem: "Wallet Verbinden" funktioniert nicht

### Symptom
- Button klickbar aber nichts passiert
- Oder Error-Message
- Oder MetaMask PopUp öffnet sich nicht

### Lösung A: MetaMask installiert?

```
Chrome: https://chromewebstore.google.com/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn
Firefox: https://addons.mozilla.org/en-US/firefox/addon/ether-metamask/
```

### Lösung B: MetaMask entsperrt?

1. MetaMask Icon oben rechts klicken
2. Falls "Locked" → Password eingeben

### Lösung C: Richtige Chain?

MetaMask könnte auf falscher Chain sein:
1. MetaMask öffnen
2. Oben "Ethereum Mainnet" klicken
3. Test-Netzwerk wählen oder Sepolia

### Lösung D: Console Errors?

```
F12 → Console → Red Errors anschauen
```

Häufige Errors:
```
❌ "Cannot read property 'ethereum' of undefined"
   → MetaMask nicht installiert

❌ "User denied account access"
   → MetaMask PopUp abgelehnt

❌ "eth_requestAccounts" failed
   → MetaMask-Error, MetaMask neu starten
```

---

## ❌ Problem: Verifizierung funktioniert nicht

### Symptom
- Wallet verbunden
- "Verifizieren" Button klickbar
- Aber nach Klick nichts passiert
- Oder Error: "Verifizierungsfehler"

### Lösung

**Schritt 1: API erreichbar?**
```bash
curl http://localhost:8000/api/verify \
  -H "Content-Type: application/json" \
  -d '{"address":"0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE"}'
```

Sollte JSON zurückgeben mit `"is_human": true`.

Falls Error → API läuft nicht!

**Schritt 2: Datenbank OK?**
```bash
sqlite3 aera.db "SELECT COUNT(*) FROM users;"
```

Sollte Zahl zurückgeben (z.B. 0 oder 5).

Falls Error → Datenbank kaputt!

**Schritt 3: Browser Console anschauen**
```
F12 → Console
Sollte zeigen: [INFO] Response Data: {...}
```

---

## ❌ Problem: Externe IP nicht erreichbar

### Symptom
- Lokal funktioniert `http://localhost:8000`
- Aber vom Smartphone `http://192.168.1.100:8000` funktioniert nicht

### Lösung

**Schritt 1: Server auf 0.0.0.0 binden**
```bash
# FALSCH:
uvicorn server:app --host 127.0.0.1 --port 8000

# RICHTIG:
uvicorn server:app --host 0.0.0.0 --port 8000
```

**Schritt 2: Externe IP finden**
```bash
hostname -I
# z.B. 192.168.1.100
```

**Schritt 3: Vom Smartphone testen**
```
http://192.168.1.100:8000
```

**Schritt 4: Firewall prüfen**
```bash
# Port 8000 freigeben
sudo ufw allow 8000
```

oder

```bash
# Firewall komplett deaktivieren (nur Testing!)
sudo ufw disable
```

---

## ❌ Problem: Port 8000 schon belegt

### Symptom
```
bind() exception: Address already in use
ERROR:     Uvicorn server failed to start. A server process is probably running already on port 8000.
```

### Lösung

**Schritt 1: Alte Prozesse finden**
```bash
ps aux | grep 8000
# oder
lsof -ti:8000
```

**Schritt 2: Prozess beenden**
```bash
# Sanft:
kill <PID>

# Erzwungen:
kill -9 <PID>

# Oder direkt:
lsof -ti:8000 | xargs kill -9
```

**Schritt 3: Neu starten**
```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

**Schritt 4: Anderen Port verwenden**
```bash
uvicorn server:app --host 0.0.0.0 --port 8001
# Dann: http://localhost:8001
```

---

## ❌ Problem: Python Import Error

### Symptom
```
ModuleNotFoundError: No module named 'fastapi'
ModuleNotFoundError: No module named 'uvicorn'
```

### Lösung

**Schritt 1: Virtual Environment aktivieren**
```bash
cd /home/karlheinz/krypto/aera-token/webside-wallet-login
source venv/bin/activate
```

Sollte so aussehen: `(venv) user@machine ~$`

**Schritt 2: Dependencies installieren**
```bash
pip install -r requirements.txt
```

**Schritt 3: Neu starten**
```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

---

## ❌ Problem: CORS Error

### Symptom
```
Access to XMLHttpRequest at 'http://localhost:8000/api/verify' 
from origin 'http://localhost:3000' has been blocked by CORS policy
```

### Lösung

CORS ist in `server.py` bereits aktiviert:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ← Erlaubt alle Origins
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Falls Problem bleibt:

**Schritt 1: .env prüfen**
```bash
cat .env | grep CORS
```

Sollte zeigen:
```
CORS_ORIGINS=*
```

**Schritt 2: Server neu starten**
```bash
pkill -f uvicorn
uvicorn server:app --host 0.0.0.0 --port 8000
```

---

## ❌ Problem: Datenbank Error

### Symptom
```
sqlite3.OperationalError: unable to open database file
sqlite3.DatabaseError: database disk image is malformed
```

### Lösung

**Schritt 1: Datenbank löschen**
```bash
rm aera.db
```

**Schritt 2: Server neu starten**
```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

Die Datenbank wird automatisch neu erstellt.

**Schritt 3: Prüfe ob neu DB erstellt wurde**
```bash
ls -la aera.db
```

Sollte Datei anzeigen.

---

## ✅ Quick Debug Checklist

```bash
# 1. Server läuft?
ps aux | grep uvicorn

# 2. Antwortet auf Requests?
curl http://localhost:8000

# 3. API erreichbar?
curl http://localhost:8000/api/health

# 4. Datenbank OK?
sqlite3 aera.db "SELECT 1;"

# 5. Ports frei?
lsof -i :8000

# 6. venv aktiviert?
which python  # Sollte venv/bin/python zeigen

# 7. Logs ansehen?
# Öffne neuen Terminal
cd webside-wallet-login
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8000 --log-level debug
```

---

## 🎯 Advanced Debugging

### Full Log Capture
```bash
cd /home/karlheinz/krypto/aera-token/webside-wallet-login
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8000 --log-level debug 2>&1 | tee server.log
```

Dann öffne Seite → Logs in `server.log` anschauen.

### Browser Network Tab
```
F12 → Network Tab
Dann jeden Request klicken für Details:
- Status Code?
- Response?
- Headers?
```

### API Test mit Postman/Insomnia
```
POST http://localhost:8000/api/verify
Headers: Content-Type: application/json
Body: {"address":"0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE"}
```

---

## 📞 Wenn nichts funktioniert

1. **Logs exportieren:**
   ```bash
   curl http://localhost:8000/api/debug | python3 -m json.tool > debug.json
   ```

2. **Browser Console Screenshot** (F12)

3. **Terminal Output kopieren:**
   ```bash
   ps aux | grep uvicorn
   sqlite3 aera.db ".tables"
   ```

4. **Alle Infos zusammen posten** mit Beschreibung des Problems

---

**AEra Login Troubleshooting © 2025 Karlheinz**
