# AEra Login v0.1 – Proof of Human via Resonance

Ein minimalistisches, Wallet-basiertes Identity-Layer-System, das beweist, dass ein Nutzer ein echter Mensch ist – **ohne KYC, ohne Klarnamen, ohne Datenweitergabe**.

---

## 🎯 Features

✅ **Wallet Login** – MetaMask & WalletConnect Support  
✅ **Resonance Score** – Intelligentes Scoring-System (0–100)  
✅ **REST API** – Einfache Verifizierung für andere Plattformen  
✅ **SQLite Datenbank** – Schnelle, lokale Persistenz  
✅ **Privacy-First** – Nur Wallet-ID + Score, keine Klardaten  
✅ **Production-Ready** – CORS-Middleware, Error-Handling, Audit-Trail  

---

## 🚀 Quick Start

### 1. Voraussetzungen

```bash
# Python 3.9+ erforderlich
python --version

# pip aktualisieren
pip install --upgrade pip
```

### 2. Installation

```bash
# In den Projektordner wechseln
cd /path/to/webside-wallet-login

# Abhängigkeiten installieren
pip install fastapi uvicorn

# (Optional) Mit requirements.txt
pip install -r requirements.txt
```

### 3. Server starten

```bash
# Development-Modus mit Auto-Reload
uvicorn server:app --reload --port 8000

# Oder Production-Modus
uvicorn server:app --host 0.0.0.0 --port 8000
```

**Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
✓ Datenbank initialisiert: /path/to/aera.db
🚀 AEra Login Server started
```

### 4. Browser öffnen

Gehe zu: **http://localhost:8000**

---

## 📋 Workflow

1. **Wallet verbinden** – Button klicken, MetaMask genehmigen
2. **Verifizieren** – Server prüft Adresse und berechnet Score
3. **Resonance Score anzeigen** – Nutzer erhält Score (50–100)
4. **Login-Token** – Für Integration in andere Plattformen

---

## 📁 Projektstruktur

```
webside-wallet-login/
├── index.html          # Frontend (HTML + JavaScript)
├── server.py           # Backend (FastAPI)
├── aera.db             # SQLite Datenbank
├── README.md           # Diese Datei
├── LICENSE             # CC BY-NC-SA 4.0
└── requirements.txt    # Python Dependencies (optional)
```

---

## 🔌 API-Endpoints

### `POST /api/verify`

Verifiziert eine Wallet-Adresse und aktualisiert den Score.

**Request:**
```json
{
  "address": "0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE"
}
```

**Response (Success):**
```json
{
  "is_human": true,
  "address": "0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE",
  "resonance_score": 51,
  "first_seen": 1700334000,
  "login_count": 2,
  "message": "Welcome back! Score increased to 51/100"
}
```

**Response (Error):**
```json
{
  "error": "Invalid address format",
  "is_human": false
}
```

---

### `GET /api/health`

Health-Check für Monitoring.

**Response:**
```json
{
  "status": "healthy",
  "service": "AEra Login v0.1",
  "timestamp": 1700334000
}
```

---

### `GET /api/user/{address}`

Ruft Benutzerdaten ab.

**Response:**
```json
{
  "address": "0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE",
  "resonance_score": 51,
  "first_seen": 1700334000,
  "last_login": 1700334120,
  "login_count": 2,
  "created_at": "2025-11-18T10:00:00"
}
```

---

### `GET /api/stats`

Öffentliche Statistiken.

**Response:**
```json
{
  "total_users": 42,
  "average_score": 65.5,
  "total_logins": 128,
  "timestamp": 1700334000
}
```

---

### `GET /api/events/{address}`

Ruft Login-Events eines Benutzers ab (bis zu 50 letzte).

**Response:**
```json
{
  "address": "0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE",
  "events": [
    {
      "id": 1,
      "address": "0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE",
      "event_type": "signup",
      "score_before": 0,
      "score_after": 50,
      "timestamp": 1700334000,
      "created_at": "2025-11-18T10:00:00"
    }
  ]
}
```

---

## 💾 Datenbank-Schema

### Tabelle: `users`

| Spalte | Typ | Beschreibung |
|--------|-----|-------------|
| `address` | TEXT (PK) | Wallet-Adresse (Unique) |
| `first_seen` | INTEGER | Unix-Timestamp des ersten Logins |
| `last_login` | INTEGER | Unix-Timestamp des letzten Logins |
| `score` | INTEGER | Resonance Score (0–100) |
| `login_count` | INTEGER | Anzahl der Logins |
| `created_at` | TEXT | ISO-Timestamp der Erstellung |

### Tabelle: `events`

| Spalte | Typ | Beschreibung |
|--------|-----|-------------|
| `id` | INTEGER (PK) | Event-ID |
| `address` | TEXT | Wallet-Adresse |
| `event_type` | TEXT | "signup" oder "login" |
| `score_before` | INTEGER | Score vor Aktion |
| `score_after` | INTEGER | Score nach Aktion |
| `timestamp` | INTEGER | Unix-Timestamp |
| `created_at` | TEXT | ISO-Timestamp |

---

## 🎓 Resonance Score Logik

Der Score beginnt bei **50** für neue Nutzer und kann bis zu **100** steigen.

- **Neuer Nutzer**: 50 Punkte
- **Jedes Login**: +1 Punkt (maximal 100)
- **Audit-Trail**: Alle Änderungen werden in der `events`-Tabelle protokolliert

**Zukünftige Erweiterungen:**
- Community-Attestierungen (+5 pro bestätigung)
- Inaktivität-Malus (-1 pro Woche ohne Login)
- On-Chain Integration (Token-Balance, Governance-Votes)

---

## 🔐 Sicherheit & Datenschutz

✅ **Keine Klardaten** – Nur Wallet-Adressen gespeichert  
✅ **Signatur-Verification** – (Wird in v0.2 hinzugefügt)  
✅ **Non-Transactional** – Kein Gasverbrauch  
✅ **HTTPS Ready** – Production-Deployment mit SSL  
✅ **Audit-Trail** – Alle Events logged  
✅ **CORS-Protection** – Konfigurierbar pro Domain  

---

## 🚀 Integration in andere Plattformen

### Beispiel: Forum-Integration

```javascript
// Forum prüft Login-Status
const response = await fetch('https://aera-login.example.com/api/user/0x742d...');
const user = await response.json();

if (user.resonance_score >= 50) {
  // Nutzer ist verifiziert → Zugang gewähren
  allowForumAccess(user.address);
}
```

### Beispiel: Discord Bot

```python
@discord.command()
async def verify(ctx):
    """Verifizierung für Discord"""
    # Wallet-Adresse erfragen
    address = await prompt_wallet(ctx)
    
    # AEra-Server abfragen
    response = requests.get(f'https://api.aera-login.com/api/user/{address}')
    user = response.json()
    
    if user.get('resonance_score', 0) >= 50:
        await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name='Verified'))
```

---

## 📝 Environment-Variablen

Optional (für Production):

```bash
# .env (create this file)
FASTAPI_ENV=production
DATABASE_URL=sqlite:///aera.db
CORS_ORIGINS=https://aera.example.com
LOG_LEVEL=info
```

---

## 🧪 Testen

### cURL-Tests

```bash
# Health-Check
curl http://localhost:8000/api/health

# Nutzer verifizieren
curl -X POST http://localhost:8000/api/verify \
  -H "Content-Type: application/json" \
  -d '{"address":"0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE"}'

# Nutzer-Daten abrufen
curl http://localhost:8000/api/user/0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE

# Statistiken abrufen
curl http://localhost:8000/api/stats
```

---

## 📦 Requirements.txt

```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
```

**Installation:**
```bash
pip install -r requirements.txt
```

---

## 🔄 Deployment (Production)

### Mit Gunicorn + Nginx

```bash
# Gunicorn installieren
pip install gunicorn

# Server starten (4 Worker)
gunicorn server:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Mit Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t aera-login .
docker run -p 8000:8000 aera-login
```

---

## 🗂️ Roadmap (v0.2+)

- ✅ v0.1 – Basis-Login, Score-System
- 🔲 v0.2 – Signatur-Verification (EIP-191)
- 🔲 v0.3 – On-Chain Integration (AEra Token Contract)
- 🔲 v0.4 – Zero-Knowledge Proofs (zk-SNARKs)
- 🔲 v0.5 – Telegram Bot Integration
- 🔲 v1.0 – Mainnet Launch + Audit

---

## 📄 Lizenz

**Creative Commons BY-NC-SA 4.0**

```
Du darfst:
✓ Verwenden und Modifizieren (für Non-Commercial Use)
✓ Mit Namensnennung (Karlheinz 2025)
✓ Unter gleicher Lizenz weitergeben

Du darfst nicht:
✗ Kommerziell verwenden
✗ Namensnennung entfernen
```

**Volltext:** https://creativecommons.org/licenses/by-nc-sa/4.0/

---

## 👤 Credits

- **Konzept & Implementierung:** Karlheinz, 2025
- **Framework:** FastAPI, ethers.js
- **Community:** AEra Project

---

## 🤝 Support

Fragen oder Bugs? Erstelle ein Issue auf GitHub oder schreibe eine E-Mail.

---

**AEra Login Prototype © 2025 Karlheinz**  
*Proving Humanity via Resonance – No KYC, No Identity Theft.*
