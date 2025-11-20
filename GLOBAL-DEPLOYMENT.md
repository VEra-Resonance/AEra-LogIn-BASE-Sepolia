# 🚀 AEra Login – Global Deployment Quick Start

Komplette Anleitung für weltweites Deployment mit QR-Code und Wallet-Support.

---

## ⚡ 60-Sekunden Start (Lokal)

```bash
cd /home/karlheinz/krypto/aera-token/webside-wallet-login

# Virtuelle Umgebung aktivieren
source venv/bin/activate

# Server starten (auf 0.0.0.0 für extern erreichbar)
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

**Dann öffnen:** `http://localhost:8000`

---

## 🌍 Global Erreichbar Machen

### Option 1: Lokales Netzwerk (LAN)

```bash
# Finde deine interne IP
hostname -I
# z.B. 192.168.1.100

# Im gleichen Netzwerk vom Smartphone aus öffnen:
# http://192.168.1.100:8000
```

---

### Option 2: Internet mit ngrok (Kostenlos, Schnell)

```bash
# 1. ngrok installieren
# Macbook: brew install ngrok
# Linux: wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip && unzip ngrok-stable-linux-amd64.zip
# Oder: https://ngrok.com/download

# 2. Auth-Token holen (kostenlos auf https://ngrok.com)
ngrok config add-authtoken YOUR_TOKEN

# 3. Tunnel öffnen
ngrok http 8000

# Output zeigt:
# Forwarding        https://abc123def456.ngrok.io -> http://localhost:8000

# 4. URL kopieren und weltweit teilen:
# https://abc123def456.ngrok.io
```

**Vorteile:**
- ✅ Kostenlos für 1-2 Stunden
- ✅ HTTPS automatisch
- ✅ Funktioniert übe Firewalls
- ✅ Sofort global erreichbar

**Nachteile:**
- ❌ URL ändert sich bei jedem Restart
- ❌ Begrenzte Sessions

---

### Option 3: Production mit Docker

```bash
# 1. Dockerfile erstellen
cat > Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV HOST=0.0.0.0
ENV PORT=8000
EXPOSE 8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# 2. Image bauen
docker build -t aera-login .

# 3. Container starten
docker run -p 8000:8000 aera-login

# URL: http://localhost:8000
```

---

### Option 4: Production mit Heroku/Railway/Replit

**Railway (Empfohlen):**

```bash
# 1. Account auf railway.app erstellen
# 2. Dieses Projekt verbinden
# 3. `.env` mit PUBLIC_URL setzen:
PUBLIC_URL=https://aera-login-xyz.railway.app

# 4. Deploy!
```

---

## 🎯 Funktionalität Testen

### Test 1: QR-Code anzeigen

```bash
# Browser öffnen → http://localhost:8000
# → QR-Code sollte sichtbar sein
# → URL sollte angezeigt werden
# → "📋 URL kopieren" Button sollte funktionieren
```

### Test 2: MetaMask Verbindung (Desktop)

```bash
# 1. Browser: http://localhost:8000
# 2. MetaMask installiert?
#    Chrome: https://chromewebstore.google.com/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn
# 3. "Wallet Verbinden" klicken
# 4. PopUp sollte erscheinen
# 5. "Genehmigen" klicken
# 6. Wallet-Adresse sichtbar
# 7. "Verifizieren" klicken
# 8. Score sollte erscheinen ✓
```

### Test 3: Mobile QR-Code

```bash
# Terminal 1: Server laufen lassen
uvicorn server:app --host 0.0.0.0 --port 8000

# Terminal 2: Externe IP finden
hostname -I
# z.B. 192.168.1.100

# Smartphone Browser öffnen:
# http://192.168.1.100:8000

# Dort sollte sichtbar sein:
# ✅ QR-Code
# ✅ URL
# ✅ "📋 URL kopieren" Button
# ✅ Tab zum Wechseln auf Desktop-Modus
```

---

## 📊 Logs & Debugging

### Server Logs anschauen

```bash
# Terminal wo Server läuft mit Ctrl+C zur Kontrolle
# Dann neu starten mit Debug-Output:
uvicorn server:app --host 0.0.0.0 --port 8000 --log-level debug
```

### Browser Console öffnen

```
F12 → Console
```

Sollte zeigen:
```
[AEra] === AEra Login gestartet ===
[AEra] URL: http://localhost:8000/
[AEra] API Base: http://localhost:8000
[AEra] Mobile: false
[AEra] QR-Code generiert für: http://localhost:8000/
[AEra] === Initialization complete ===
```

### API Test

```bash
# Health Check
curl http://localhost:8000/api/health

# Wallet verifizieren
curl -X POST http://localhost:8000/api/verify \
  -H "Content-Type: application/json" \
  -d '{"address":"0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE"}'

# Statistiken
curl http://localhost:8000/api/stats
```

---

## 🔧 Konfiguration für Production

### .env anpassen

```bash
# Vor Production-Deployment
nano .env
```

Wichtige Werte:

```env
# Externe URL (für QR-Code & Links)
PUBLIC_URL=https://aera-login.example.com

# Server auf alle Interfaces binden
HOST=0.0.0.0
PORT=8000

# CORS Origins (nur deine Domains)
CORS_ORIGINS=https://aera-login.example.com,https://app.example.com

# Logging
LOG_LEVEL=info

# Resonance Score Config
INITIAL_SCORE=50
MAX_SCORE=100
SCORE_INCREMENT=1
```

### HTTPS aktivieren (Production Pflicht!)

**Mit Let's Encrypt (kostenlos):**

```bash
# 1. Certbot installieren
pip install certbot

# 2. Zertifikat generieren
certbot certonly --standalone -d aera-login.example.com

# 3. Server mit SSL starten
uvicorn server:app \
  --host 0.0.0.0 \
  --port 8443 \
  --ssl-keyfile=/etc/letsencrypt/live/aera-login.example.com/privkey.pem \
  --ssl-certfile=/etc/letsencrypt/live/aera-login.example.com/fullchain.pem
```

---

## 📱 Smartphone Test

### iPhone/iPad

```
1. Safari öffnen
2. URL eingeben: http://192.168.X.X:8000
3. Seite sollte laden
4. QR-Code sichtbar
5. Im Wallet öffnen → MetaMask
```

### Android

```
1. Chrome öffnen
2. URL eingeben: http://192.168.X.X:8000
3. Seite sollte laden
4. QR-Code sichtbar
5. MetaMask App: "Browser" Tab → URL eingeben
```

---

## 🐛 Troubleshooting

### Problem: "Connection refused"

```bash
# Prüfe ob Server läuft
ps aux | grep uvicorn

# Falls nicht, starte neu
uvicorn server:app --host 0.0.0.0 --port 8000
```

### Problem: QR-Code nicht sichtbar

```bash
# Browser Console öffnen (F12)
# Sollte Fehler zeigen, z.B. "Canvas not found"
# Seite neu laden: Ctrl+R / Cmd+R
```

### Problem: MetaMask PopUp öffnet sich nicht

```bash
# 1. MetaMask installiert?
# 2. MetaMask entsperrt?
# 3. Richtige Chain?
# 4. Browser erlaubt PopUps?
# Browser Settings → PopUp Blocker → Erlauben
```

### Problem: Wallet-Verbindung funktioniert auf localhost nicht

```bash
# MetaMask funktioniert nur auf:
# ✅ http://localhost:8000 (lokal)
# ✅ https://example.com (HTTPS)
# ✅ 127.0.0.1:8000 (lokal)
# ❌ http://192.168.1.100:8000 (HTTP + externe IP = geblockt!)

# Lösung für mobiles Testing:
# Option A: ngrok nutzen (HTTPS)
# Option B: HTTPS mit selbst-signiertem Cert
# Option C: Lokal auf dem Gerät testen
```

---

## 📈 Scaling für Millionen Nutzer

Wenn du global skalierst:

1. **Database:** SQLite → PostgreSQL
2. **Server:** Single Instance → Load Balanced (Nginx)
3. **Caching:** Redis für häufige Abfragen
4. **CDN:** CloudFlare für Assets
5. **Monitoring:** Sentry für Error Tracking
6. **Analytics:** PostHog oder Mixpanel

---

## 🎓 Nächste Schritte

- [ ] QR-Code auf der Seite sichtbar?
- [ ] URL angezeigt?
- [ ] Wallet verbindbar (Desktop)?
- [ ] Verifizierung funktioniert?
- [ ] Score wird berechnet?
- [ ] Lokal im Netzwerk erreichbar?
- [ ] Mit ngrok global erreichbar?
- [ ] Auf echtem Smartphone getestet?
- [ ] Production URL konfiguriert?
- [ ] HTTPS aktiviert?

---

## 📞 Support

Fragen? Logs posten:

```bash
# Logs exportieren
uvicorn server:app --host 0.0.0.0 --port 8000 2>&1 | tee logs.txt

# Browser Console (F12) → Screenshot machen
# Error Messages teilen
```

---

**AEra Login Global Edition © 2025 Karlheinz** ⸻ *Registration from anywhere, for everyone*
