# 📱 AEra Login Mobile Setup Guide

Vollständige Anleitung für Mobile-Registrierung mit QR-Code und Deep-Links.

---

## 🎯 Features

✅ **Auto Mobile Detection** – Erkennt automatisch wenn via Smartphone zugegriffen wird  
✅ **QR-Code Generation** – Generiert QR-Codes zum Scannen mit Desktop-Wallets  
✅ **Deep Links** – Direktes Öffnen in MetaMask/TrustWallet auf dem Smartphone  
✅ **Responsive Design** – Optimiert für alle Bildschirmgrößen  
✅ **Offline-Ready** – Funktioniert auch mit Schwachverbindung  

---

## 📱 Szenarios

### Szenario 1: Desktop Browser (MetaMask Extension)

**So funktioniert es:**

1. Öffne `http://localhost:8000` im **Desktop Browser**
2. MetaMask wird automatisch erkannt
3. Klick auf "Wallet Verbinden" → MetaMask PopUp öffnet sich
4. "Genehmigen" klicken
5. Wallet-Adresse wird angezeigt
6. Klick auf "Verifizieren" → Score wird berechnet

**Logs:**
```
INFO: GET / HTTP/1.1 200 OK
INFO: Client requesting wallet connection (Desktop detected)
INFO: eth_requestAccounts called successfully
INFO: POST /api/verify - Address verified, score: 50
```

---

### Szenario 2: Smartphone mit Wallet-App (MetaMask Mobile)

**So funktioniert es:**

1. Öffne `http://localhost:8000` (oder den Server über externe IP)
2. **Mobile wird automatisch erkannt** → QR-Code + "In Wallet öffnen" Button
3. Option A: Klick auf "In Wallet öffnen" → MetaMask öffnet sich automatisch
4. Option B: Scanne den QR-Code mit Desktop-Wallet
5. Wallet-Verbindung etabliert
6. Verifizierung und Score-Berechnung

**Deep Link Format:**
```
https://metamask.app.link/dapp/your-domain.com
```

---

### Szenario 3: Smartphone Browser (kein MetaMask)

**So funktioniert es:**

1. Öffne `http://localhost:8000` im Smartphone Browser
2. Mobile wird erkannt, aber **keine Wallet-App gefunden**
3. QR-Code wird angezeigt
4. **Optionen:**
   - Scanne QR mit Desktop-PC
   - Installiere MetaMask App (Link wird angezeigt)
   - Nutze "In TrustWallet öffnen" Button

**QR-Code enthält:**
- Seiten-URL
- Wallet-Addresse (fallback)
- Deep-Links zu Wallet-Apps

---

## 🔧 Technische Implementation

### Mobile Detection Logic

```javascript
function detectMobile() {
    const userAgent = navigator.userAgent || navigator.vendor || window.opera;
    const isMobileDevice = /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(userAgent.toLowerCase());
    const isSmallScreen = window.innerWidth <= 768px;
    return isMobileDevice || isSmallScreen;
}
```

**Erkannt als "Mobile":**
- ✅ iPhone, iPad, Android
- ✅ Tablets (iPad, Samsung Tab)
- ✅ Screen < 768px Breite
- ❌ Desktop PCs (auch bei Edge)

---

### QR-Code Generation

**Library:** QRious.js (CDN)

```javascript
function generateQRCode(text) {
    new QRious({
        element: document.getElementById('qrCode'),
        size: 300,
        value: text,  // Seiten-URL
        level: 'H',   // Höchste Fehlerkorrektur
        background: '#ffffff',
        foreground: '#667eea'  // AEra-Farbe
    });
}
```

**QR-Code Payload:**
```
http://localhost:8000
```

oder mit Parameter:
```
http://localhost:8000?affiliate=0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE
```

---

### Deep-Link Handling

**MetaMask (iOS & Android):**
```javascript
const deepLink = `https://metamask.app.link/dapp/${window.location.hostname}${window.location.pathname}`;
```

**TrustWallet:**
```javascript
const deepLink = `trust://browser_enable?url=${encodeURIComponent(window.location.href)}`;
```

**WalletConnect (Universal):**
```javascript
const wc = `wc:app@1?name=AEraLogin&description=Verify your identity`;
```

---

## 🧪 Testing

### Test 1: Desktop (Chrome/Firefox/Safari)

```bash
# 1. Terminal öffnen
cd /path/to/webside-wallet-login
source venv/bin/activate
uvicorn server:app --reload --port 8000

# 2. Browser öffnen
http://localhost:8000

# 3. MetaMask Test
- Extension sollte erkannt werden
- Wallet Verbinden klicken
- PopUp sollte erscheinen
```

**Erwartet:** ✅ MetaMask PopUp erscheint

---

### Test 2: Mobile (Simulator)

**Chrome DevTools:**
```
F12 → Toggle Device Toolbar → Ctrl+Shift+M
```

Dann im Emulator:
1. Öffne Developer Console (F12)
2. Gehe zu `http://localhost:8000`
3. QR-Code sollte sichtbar sein
4. Console sollte zeigen: `Mobile-Modus erkannt`

**Erwartet:**
- ✅ QR-Code angezeigt
- ✅ "In Wallet öffnen" Button
- ✅ "📱 Mobile-Modus erkannt"

---

### Test 3: Echtes Smartphone

**Voraussetzung:** Server mit externer IP erreichbar

```bash
# 1. Externe IP finden
hostname -I

# 2. Server auf alle Interfaces binden
uvicorn server:app --host 0.0.0.0 --port 8000

# 3. Im Smartphone-Browser öffnen
http://YOUR_EXTERNAL_IP:8000

# 4. MetaMask App öffnen
- App öffnet sich automatisch
- Verifizierung durchführen
```

**Erwartet:** ✅ Volle Funktionalität auf Echtgerät

---

### Test 4: QR-Code Scan

```bash
# 1. QR-Code im Browser anzeigen lassen (Mobile)
# 2. Mit anderem Gerät Webcam QR-Scanner öffnen
# 3. Scannen → Link sollte automatisch öffnen
```

**QR-Scanner Tools:**
- ✅ Builtin iPhone Camera App
- ✅ Google Lens
- ✅ WeChat
- ✅ Online QR-Scanner (qr-code-generator.com)

---

## 🌐 Deployment für Mobile

### Lokal Testen (nur LAN)

```bash
# Server auf allen Interfaces binden
uvicorn server:app --host 0.0.0.0 --port 8000

# Dann vom Smartphone aus:
# http://192.168.1.100:8000  (deine Router-IP)
```

---

### Production (Internet-erreichbar)

**Mit ngrok (Tunnel):**

```bash
# 1. ngrok installieren (https://ngrok.com)
ngrok config add-authtoken YOUR_TOKEN

# 2. Tunnel starten
ngrok http 8000

# 3. Public URL kopieren
# https://abc123.ngrok.io

# 4. Vom Smartphone öffnen
# https://abc123.ngrok.io
```

---

**Mit eigenem Server (AWS/Heroku/DigitalOcean):**

```bash
# 1. Deployment vorbereiten (siehe README.md → Deployment)
# 2. HTTPS aktivieren (Let's Encrypt)
# 3. CORS auf deine Domain konfigurieren

# In server.py:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aera-login.example.com"],  # ← Deine Domain
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 Mobile-spezifische API-Responses

### Beim Mobile Zugriff (automatisch erkannt)

**Response zu `/` (HTML):**
```html
<!-- QR-Code Canvas wird gerendert -->
<!-- Deep-Links werden generiert -->
<!-- Mobile-spezifisches UI wird gezeigt -->
```

**Browser Console Logs:**
```
[AEra] Mobile device detected
[AEra] Generating QR code for: http://localhost:8000
[AEra] MetaMask deep link: https://metamask.app.link/dapp/localhost
```

---

### Debug-Informationen

```bash
# Server Debug Endpoint
curl http://localhost:8000/api/debug
```

**Response:**
```json
{
  "server": "AEra Login v0.1",
  "client_ip": "192.168.1.50",
  "mobile_detection": "enabled",
  "qr_code_support": "yes"
}
```

---

## 🔐 Sicherheits-Aspekte bei Mobile

✅ **HTTPS Pflicht** – Alle Wallet-Verbindungen müssen über HTTPS laufen  
✅ **Deep-Links validieren** – Nur offiziell signierte Deep-Links akzeptieren  
✅ **QR-Code expiration** – QR-Codes sollten nach 5 min verfallen  
✅ **Mobile-Device-IDs** – Optional: Geräte-Fingerprinting gegen Farming  
✅ **Rate Limiting** – Max. 5 Verifizierungen pro Minute pro Device  

---

## 🐛 Troubleshooting Mobile

### Problem: MetaMask öffnet sich nicht nach QR-Scan

**Lösung:**
```javascript
// In server.py Deep-Link korrigieren:
deepLink = `https://metamask.app.link/dapp/${window.location.host}/`
// ↑ Sicherstelle dass Trailing Slash dabei ist
```

---

### Problem: QR-Code wird nicht angezeigt

**Lösung:**
```javascript
// QRious.js wird nicht geladen? 
// In index.html:
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrious/4.0.2/qrious.min.js"></script>
// ↑ Prüfe ob CDN erreichbar ist
```

---

### Problem: "Connection refused" auf echtem Smartphone

**Lösung:**
```bash
# Server muss auf 0.0.0.0 binden, nicht nur 127.0.0.1
uvicorn server:app --host 0.0.0.0 --port 8000

# Deine interne IP finden:
hostname -I

# Dann im Smartphone-Browser:
http://192.168.X.X:8000
```

---

### Problem: HTTPS-Zertifikat Fehler

**Für lokale Tests mit HTTPS:**

```bash
# Self-signed Cert generieren
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Server mit SSL starten
uvicorn server:app --host 0.0.0.0 --port 8443 --ssl-keyfile=key.pem --ssl-certfile=cert.pem
```

---

## 📚 Weitere Ressourcen

- **MetaMask Mobile Docs:** https://docs.metamask.io/guide/mobile-best-practices.html
- **QRious.js:** https://davidshimjs.github.io/qrcodejs/
- **Deep Linking:** https://www.geeksforgeeks.org/deep-linking-in-android/
- **Mobile Web Best Practices:** https://developers.google.com/web/tools/lighthouse/audits/viewport

---

**AEra Login Mobile © 2025 Karlheinz** ⸻ *Registration from anywhere, for anyone*
