# 🚀 AEra Login – Installation & Quick Start Guide

Vollständige Anleitung zum Starten des AEra Login Systems.

---

## 📋 Inhaltsverzeichnis

1. [Systemvoraussetzungen](#systemvoraussetzungen)
2. [Installation Schritt-für-Schritt](#installation-schrittfürschritt)
3. [Server starten](#server-starten)
4. [Testen & Verifizieren](#testen--verifizieren)
5. [Troubleshooting](#troubleshooting)

---

## 🖥️ Systemvoraussetzungen

### Erforderlich
- **Python 3.9+** (oder 3.11)
- **pip** (Python Package Manager)
- **Git** (zum klonen, optional)
- **MetaMask** oder eine andere EVM-kompatible Wallet (für Frontend-Tests)

### Empfohlen
- **Virtual Environment** (venv) – für Isolation
- **Postman oder cURL** – für API-Tests
- **VS Code oder IDE** – zum Bearbeiten

### Optional
- **Docker** – für containerisiertes Deployment
- **PostgreSQL** – für Production (statt SQLite)

---

## 📦 Installation Schritt-für-Schritt

### Schritt 1: Repository klonen / In Ordner gehen

```bash
# Falls noch nicht im webside-wallet-login Ordner:
cd /path/to/webside-wallet-login
```

### Schritt 2: Virtuelle Umgebung erstellen (EMPFOHLEN)

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows (CMD)
python -m venv venv
venv\Scripts\activate

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
```

**Ausgabe sollte so aussehen:**
```
(venv) user@machine ~/webside-wallet-login $
```

### Schritt 3: pip aktualisieren

```bash
pip install --upgrade pip
```

### Schritt 4: Abhängigkeiten installieren

**Option A: Mit requirements.txt**
```bash
pip install -r requirements.txt
```

**Option B: Manuell**
```bash
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install pydantic==2.5.0
pip install python-dotenv==1.0.0
```

**Ausgabe sollte so aussehen:**
```
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 pydantic-2.5.0 ...
```

### Schritt 5: Installation verifizieren

```bash
python -c "import fastapi; import uvicorn; print('✓ All imports OK')"
```

**Erwartet:** `✓ All imports OK`

---

## 🚀 Server starten

### Methode A: Einfach (Empfohlen)

```bash
# Stelle sicher, dass deine venv aktiviert ist
source venv/bin/activate  # oder äquivalent für dein OS

# Starte den Server
uvicorn server:app --reload --port 8000
```

**Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Methode B: Mit Shell-Script

```bash
./start.sh
```

(Das Script aktiviert venv automatisch)

### Methode C: Mit Auto-Reload deaktiviert

```bash
uvicorn server:app --port 8000
```

(Schneller, aber Code-Änderungen brauchen Restart)

---

## 🧪 Testen & Verifizieren

### Test 1: Health-Check (Terminal)

```bash
# Öffne ein NEUES Terminal-Tab/Fenster
curl http://localhost:8000/api/health | python -m json.tool
```

**Erwartet:**
```json
{
  "status": "healthy",
  "service": "AEra Login v0.1",
  "timestamp": 1234567890
}
```

---

### Test 2: Frontend öffnen (Browser)

Gehe zu: **http://localhost:8000**

Du solltest sehen:
- ✅ AEra Logo
- ✅ "Wallet Verbinden" Button
- ✅ "Proof of Human via Resonance" Text

---

### Test 3: Wallet-Verbindung (Browser)

1. **MetaMask öffnen** – Stelle sicher, dass MetaMask installiert ist
2. **"Wallet Verbinden" klicken**
3. **Genehmigung in MetaMask geben**
4. Du solltest deine Wallet-Adresse sehen ✓

---

### Test 4: Verifizierung (Browser)

1. **Nach erfolgreicher Wallet-Verbindung:** "Verifizieren" Button klicken
2. **Server antwortet mit Score:** z.B. "Score: 50/100" ✓
3. **Details anzeigen:** Adresse, Netzwerk, Score

---

### Test 5: API-Calls (cURL)

```bash
# Wallet-Adresse verifizieren
curl -X POST http://localhost:8000/api/verify \
  -H "Content-Type: application/json" \
  -d '{"address":"0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE"}'
```

**Erwartet:**
```json
{
  "is_human": true,
  "address": "0x742d35cc6634c0532925a3b844bc59e7e6d6e0de",
  "resonance_score": 50,
  "first_seen": 1234567890,
  "login_count": 1,
  "message": "Welcome! Your initial Resonance Score is 50/100"
}
```

---

### Test 6: Mehrfach-Verifizierung

Führe denselben curl-Command nochmal aus:

```bash
curl -X POST http://localhost:8000/api/verify \
  -H "Content-Type: application/json" \
  -d '{"address":"0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE"}'
```

**Erwartet:** Score ist jetzt **51** (erhöht um 1) ✓

---

## 🛠️ Troubleshooting

### Problem: "Port 8000 already in use"

**Lösung A:** Beende andere Prozesse auf Port 8000
```bash
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# oder einen anderen Port verwenden
uvicorn server:app --port 8001
```

**Lösung B:** Browser auf neuem Port öffnen
```
http://localhost:8001
```

---

### Problem: "ModuleNotFoundError: No module named 'fastapi'"

**Lösung:** Virtuelle Umgebung aktivieren
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

# Dann nochmal Abhängigkeiten installieren
pip install -r requirements.txt
```

---

### Problem: "Connection refused" beim cURL-Test

**Lösung:** Server läuft nicht
```bash
# Prüfe ob Server läuft
ps aux | grep uvicorn

# Falls nicht, starte ihn neu
uvicorn server:app --port 8000
```

---

### Problem: MetaMask Connect Button funktioniert nicht

**Lösung 1:** MetaMask Erweiterung installieren
- Chrome: https://chromewebstore.google.com/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn

**Lösung 2:** Entwickler-Konsole checken
- Browser öffnen: F12 → Console
- Fehler-Meldungen schauen

**Lösung 3:** Browser-Cache leeren
```
Ctrl+Shift+Delete → Cookies & Cache
```

---

### Problem: CORS-Fehler im Browser

**Anzeichen:**
```
Access to XMLHttpRequest at 'http://localhost:8000/api/verify' 
from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Lösung:** CORS ist bereits in `server.py` aktiviert. Falls Problem bleibt:
```python
# In server.py nach Zeile 16 prüfen:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ← muss so sein
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Problem: Datenbank-Fehler

**Anzeichen:** `sqlite3.OperationalError`

**Lösung:** Datenbank zurücksetzen
```bash
# Lösche alte DB
rm aera.db

# Starte Server neu
uvicorn server:app --reload --port 8000
```

Die Datenbank wird automatisch neu erstellt.

---

## 📊 Logs & Debugging

### Server-Logs im Detail

```bash
# Mit mehr Debug-Info
uvicorn server:app --reload --port 8000 --log-level debug
```

### Browser-Konsole

```javascript
// Im Browser öffnen: F12 → Console
// Dann testen:
fetch('http://localhost:8000/api/health')
  .then(r => r.json())
  .then(d => console.log('✓ Server OK:', d))
  .catch(e => console.error('✗ Error:', e))
```

### SQLite Datenbank inspizieren

```bash
# SQLite CLI öffnen
sqlite3 aera.db

# Dann in der Konsole:
> SELECT * FROM users;
> SELECT * FROM events;
> .quit
```

---

## ✅ Checkliste: Alles läuft?

- [ ] Python 3.9+ installiert
- [ ] Virtual Environment erstellt & aktiviert
- [ ] `pip install -r requirements.txt` erfolgreich
- [ ] `uvicorn server:app --reload --port 8000` startet
- [ ] `curl http://localhost:8000/api/health` antwortet
- [ ] Browser öffnet `http://localhost:8000`
- [ ] Wallet Verbinden Button sichtbar
- [ ] MetaMask Wallet verbunden ✓
- [ ] Verifizierung funktioniert
- [ ] Score steigt bei mehrfachen Verifizierungen

---

## 🎉 Geschafft!

Du hast AEra Login erfolgreich installiert! 🚀

### Nächste Schritte:

1. **Integration in andere Plattformen** – Nutze die `/api/verify` Endpoint
2. **Customization** – Passe Farben, Logo, Score-Logik an
3. **Production Deployment** – Siehe `README.md` → Deployment-Sektion
4. **On-Chain Integration** – Verbinde mit AEra Token Smart Contract

---

## 📞 Support & Links

- **GitHub:** [aera-token/webside-wallet-login](https://github.com/example)
- **Docs:** Siehe `README.md`
- **License:** CC BY-NC-SA 4.0 (siehe `LICENSE`)
- **Kontakt:** Karlheinz (2025)

---

**AEra Login © 2025 Karlheinz** ⸻ *Proving Humanity via Resonance*
