# 🚀 AEra Login – START HIER

## Schnelle Links

| Link | Beschreibung |
|------|-------------|
| 📖 [README.md](README.md) | Vollständige Dokumentation |
| ⚙️ [INSTALLATION.md](INSTALLATION.md) | Schritt-für-Schritt Installation |
| 📱 [MOBILE-SETUP.md](MOBILE-SETUP.md) | Mobile & QR-Code Setup |
| 🌍 [GLOBAL-DEPLOYMENT.md](GLOBAL-DEPLOYMENT.md) | Global erreichbar machen |
| ✅ [CHECKLIST.md](CHECKLIST.md) | Funktions-Checklist |

---

## 60-Sekunden Quick Start

```bash
# 1. In den Ordner gehen
cd /home/karlheinz/krypto/aera-token/webside-wallet-login

# 2. Virtuelle Umgebung aktivieren
source venv/bin/activate

# 3. Server starten
uvicorn server:app --host 0.0.0.0 --port 8000 --reload

# 4. Browser öffnen
# http://localhost:8000
```

---

## Was soll funktionieren?

✅ **QR-Code sichtbar** – Im "📱 QR-Code" Tab  
✅ **URL angezeigt** – Unter QR-Code  
✅ **Wallet verbindbar** – Desktop mit MetaMask  
✅ **Verifizierung funktioniert** – Score wird berechnet  
✅ **Logins gezählt** – Bei mehrfachen Verifizierungen  

---

## Probleme?

1. **QR-Code nicht sichtbar?**
   - Browser F12 → Console
   - Sollte Logs zeigen
   - Seite neu laden (Ctrl+R)

2. **Wallet verbindet nicht?**
   - MetaMask installiert?
   - MetaMask entsperrt?
   - Auf http://localhost:8000 testen

3. **API nicht erreichbar?**
   - `curl http://localhost:8000/api/health`
   - Server läuft?
   - Port 8000 frei?

---

## Dateistruktur

```
webside-wallet-login/
├── index.html                    # Frontend (HTML+JS)
├── server.py                     # Backend (FastAPI)
├── aera.db                       # SQLite Datenbank
├── .env                          # Konfiguration
├── requirements.txt              # Python Dependencies
├── venv/                         # Virtuelle Umgebung
│
├── README.md                     # Vollständige Docs
├── INSTALLATION.md               # Installation
├── MOBILE-SETUP.md              # Mobile Setup
├── GLOBAL-DEPLOYMENT.md         # Production
├── CHECKLIST.md                 # Tests
└── START.md                      # Diese Datei
```

---

## API Endpoints

| Methode | Endpoint | Beschreibung |
|---------|----------|-------------|
| GET | `/` | Frontend HTML |
| GET | `/api/health` | Health Check |
| POST | `/api/verify` | Wallet verifizieren |
| GET | `/api/user/{address}` | Nutzer-Daten |
| GET | `/api/stats` | Statistiken |
| GET | `/api/events/{address}` | Login-History |

---

## Environment Konfiguration

Wichtigste `.env` Variablen:

```env
# Server
HOST=0.0.0.0          # 0.0.0.0 = extern erreichbar
PORT=8000
PUBLIC_URL=http://localhost:8000

# Für Production
PUBLIC_URL=https://aera-login.example.com

# CORS
CORS_ORIGINS=*        # "*" für Development
```

---

## Nächste Schritte

1. ✅ Lokal starten (`http://localhost:8000`)
2. ✅ QR-Code & URL überprüfen
3. ✅ Wallet verbinden & verifizieren
4. ✅ Mit ngrok global erreichbar machen
5. ✅ [CHECKLIST.md](CHECKLIST.md) durchgehen
6. ✅ Production deployen

---

## Support

**Logs anschauen:**
```bash
# Terminal mit Server
# Drücke Ctrl+C um zu stoppen
# Neu starten mit Debug:
uvicorn server:app --host 0.0.0.0 --port 8000 --log-level debug
```

**Browser Console:**
```
F12 → Console
Sollte Logs mit [AEra] Prefix zeigen
```

**API Test:**
```bash
curl http://localhost:8000/api/health | python3 -m json.tool
```

---

## Lizenz

CC BY-NC-SA 4.0 – Siehe [LICENSE](LICENSE)

---

**AEra Login © 2025 Karlheinz**  
*Proof of Human via Resonance – Global Edition*
