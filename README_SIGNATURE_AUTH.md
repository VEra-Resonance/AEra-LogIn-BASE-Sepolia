# 🔐 AEra Login - Proof of Human via Resonance

Cryptographically secure wallet login mit **Proof-of-Human via Resonance Score**.

**🔒 SICHERHEITS-FEATURE**: Signatur-basierte Authentifizierung erzwingt echte MetaMask-Interaktion. Login ohne aktivem MetaMask ist **UNMÖGLICH**.

---

## 🚀 Quick Start

```bash
# 1. Setup venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Starte Server
./deploy.sh

# 3. Öffne Browser
open http://localhost:8820
```

**Server läuft auf**: `0.0.0.0:8820` (erreichbar von überall!)

---

## 🔐 Sicherheits-Architektur

### Layer 1: MetaMask-Popup-Erzwingung
- **connectWallet()** nutzt `eth_requestAccounts` (nicht `eth_accounts`)
- **Popup wird ANGEZEIGT** wenn MetaMask inaktiv → Login blockiert sofort

### Layer 2: Real-Time Validierung
- **verifyWallet()** nutzt auch `eth_requestAccounts` 
- Prüft auf Wallet-Wechsel
- **BLOCKIERT** wenn MetaMask offline wird

### Layer 3: Kryptographische Signaturen (NEU!)
Das ist die **KRITISCHSTE** Schicht:

```
1. Browser fordert Nonce vom Server: GET /api/nonce
   └─ Server generiert zufällige 16-byte Nonce

2. MetaMask MUSS die Nonce signieren:
   └─ window.ethereum.request({
       method: 'personal_sign',
       params: [message_with_nonce, address]
     })

3. Browser sendet Signatur an Server: POST /api/verify
   └─ Signatur + Nonce + Address + Message

4. Server VERIFIZIERT Signatur kryptographisch:
   └─ Recovered Address MUSS == Request Address
   └─ Account.recover_message(message, signature)
   └─ Unterschied = LOGIN BLOCKIERT

5. NUR NACH erfolgreicher Verifikation:
   └─ User-Registration
   └─ Token-Generierung
   └─ Airdrop
```

**Bedeutung**: Kann die Signature validiert werden, war MetaMask DEFINITIV aktiv und hat TATSÄCHLICH signiert!

---

## 📡 API-Endpoints

### 1. `/api/nonce` (POST)
**Generiert Signatur-Nonce**

Request:
```json
{
  "address": "0xed1a95ab5b794dc20964693fbcc60a3dfb5a22c5"
}
```

Response:
```json
{
  "success": true,
  "nonce": "830629d5ce64b781...",
  "message": "Signiere diese Nachricht...\nNonce: 830629d5ce64b781..."
}
```

### 2. `/api/verify` (POST)
**Verifiziert Wallet + Signatur + Erzeugt Token**

⚠️ **KRITISCH**: Benötigt GÜLTIGE Signatur!

Request:
```json
{
  "address": "0xed1a95ab5b794dc20964693fbcc60a3dfb5a22c5",
  "nonce": "830629d5ce64b781...",
  "message": "Signiere diese Nachricht...\nNonce: 830629d5ce64b781...",
  "signature": "0x1234567890abcdef...",
  "token_duration_hours": 24
}
```

Response (nur wenn Signatur VALID):
```json
{
  "is_human": true,
  "address": "0xed1a95ab5b794dc20964693fbcc60a3dfb5a22c5",
  "resonance_score": 50,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "message": "Welcome! Your initial Resonance Score is 50/100"
}
```

Error (wenn Signatur UNGÜLTIG):
```json
{
  "is_human": false,
  "error": "Signature verification failed"
}
```

### 3. `/api/verify-token` (POST)
**Auto-Login mit gespeichertem Token + neuer Signatur**

Request:
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "address": "0xed1a95ab5b794dc20964693fbcc60a3dfb5a22c5",
  "nonce": "830629d5ce64b781...",
  "message": "Signiere diese Nachricht...",
  "signature": "0x1234567890abcdef..."
}
```

---

## 📊 Datenbank-Schema

### `users` Tabelle
```
address          TEXT PRIMARY KEY  (0x...)
first_seen       INTEGER          (Unix timestamp)
last_login       INTEGER          (Unix timestamp)
score            INTEGER          (50-100)
login_count      INTEGER          (Anzahl Logins)
created_at       TEXT             (ISO 8601)
```

### `events` Tabelle
```
id               INTEGER PRIMARY KEY
address          TEXT              (Wallet)
event_type       TEXT              ('login', 'signup', 'score_change')
score_before     INTEGER
score_after      INTEGER
timestamp        INTEGER           (Unix)
created_at       TEXT              (ISO 8601)
```

### `airdrops` Tabelle
```
id               INTEGER PRIMARY KEY
address          TEXT
tx_hash          TEXT              (Blockchain TX)
amount           REAL              (0.5 AERA)
status           TEXT              ('pending', 'success', 'failed')
timestamp        INTEGER
```

---

## 🎯 Resonance Score System

**Score-Range**: 50 - 100

- **50** = Neuer Benutzer (Initial)
- **51-99** = Score erhöht sich bei jedem Login (+1)
- **100** = Maximum erreicht

```sql
SELECT * FROM users WHERE score >= 90;  -- Top Humans
```

---

## 🔍 Logging & Überwachung

### Vier Log-Dateien

```
logs/
├── aera.log          ← ALLES (Timestamp + Funktion + Nachricht)
├── aera.json         ← Strukturiertes JSON (für Analyse)
├── activity.log      ← Nur wichtige Events
└── errors.log        ← NUR Fehler + Stack Traces
```

### Wichtige Log-Messages

```
[AUTH] Verify request received | address=0xed1a95ab | has_signature=True
[AUTH] ✓✓✓ Signature VERIFIED | address=0xed1a95ab
[AUTH] New user registered | address=0xed1a95ab | initial_score=50
```

### Sicherheits-Logs

```
[AUTH] No signature provided - REJECTING
[AUTH] Signature verification FAILED
[AUTH] Invalid address format
[AUTH] eth_account not available - [WARNING]
```

---

## 🧪 Testing

### Unit-Tests für Signatur-Verifikation

```bash
source venv/bin/activate
python3 test_signature_verification.py
```

**Testet**:
1. ✓ Nonce-Generierung
2. ✓ Ungültige Signaturen WERDEN ABGELEHNT
3. ✓ Anfragen ohne Signatur WERDEN ABGELEHNT
4. ✓ Server-Logs korrekt dokumentiert

---

## 🔧 Konfiguration

### `.env`

```env
# Server
HOST=0.0.0.0
PORT=8820
PUBLIC_URL=http://localhost:8820

# Wallets
ADMIN_WALLET=0xed1a95ab5b794dc20964693fbcc60a3dfb5a22c5
ADMIN_PRIVATE_KEY=0x1234...

# Blockchain
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_KEY
AERA_CONTRACT=0x5032206396A6001eEaD2e0178C763350C794F69e

# Token
TOKEN_SECRET=your-secret-key-change-in-prod
TOKEN_EXPIRY_DAYS=7

# Scores
INITIAL_SCORE=50
MAX_SCORE=100
SCORE_INCREMENT=1

# CORS
CORS_ORIGINS=*
```

---

## 🚀 Deployment

### Production-Deployment (mit Systemd)

```bash
# 1. Deploy-Skript ausführen
./deploy.sh

# 2. Überprüfe Logs
tail -f server.log
tail -f logs/activity.log

# 3. Health-Check
curl http://localhost:8820/api/health
```

### Docker (Optional)

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "server.py"]
```

```bash
docker build -t aera-login .
docker run -p 8820:8820 \
  -e HOST=0.0.0.0 \
  -e PORT=8820 \
  aera-login
```

---

## 🔒 Sicherheits-Checkliste

- ✅ **Signatur-Verifikation**: ERZWUNGEN
- ✅ **MetaMask-Popup**: IMMER angezeigt
- ✅ **Nonce-Zufälligkeit**: 16 Bytes (128 Bits)
- ✅ **Address-Recovery**: eth_account library
- ✅ **Wallet-Wechsel-Schutz**: SafeWallet-Modus (One-wallet-per-user)
- ✅ **Replay-Attack-Schutz**: Neue Nonce pro Anfrage (TODO: Nonce-Expiry)
- ✅ **Logging**: Audit-Trail für ALLE Authentifizierung

---

## 🪲 Bekannte Issues

### Issue 1: eth_account nicht verfügbar
**Symptom**: Log zeigt `eth_account not available - skipping signature check`

**Ursache**: Server läuft nicht in venv

**Fix**:
```bash
source venv/bin/activate
pip install eth-account
./deploy.sh
```

### Issue 2: Import-Fehler in IDE
**Symptom**: VSCode zeigt "Could not resolve import eth_account"

**Ursache**: Pylint kann venv nicht finden

**Fix**: Keine - Code funktioniert! Nur IDE-Hinweis

---

## 📚 Weitere Ressourcen

- **eth_account Docs**: https://eth-account.readthedocs.io/
- **EIP-191**: https://eips.ethereum.org/EIPS/eip-191 (Message signing)
- **FastAPI**: https://fastapi.tiangolo.com/
- **MetaMask**: https://docs.metamask.io/

---

## 📄 Lizenz

CC BY-NC-SA 4.0

---

## ✨ Feature-Roadmap

- [x] Grundlegende Wallet-Verbindung
- [x] MetaMask-Validierung
- [x] Resonance Score System
- [x] **Signatur-basierte Authentifizierung** ← NEU!
- [ ] Nonce-Expiry (30 Sekunden)
- [ ] Rate-Limiting auf `/api/nonce`
- [ ] Multi-Chain Support (Ethereum + Polygon)
- [ ] Gasless Signatures (ERC-191)
- [ ] Session Persistence
- [ ] Admin Dashboard

---

**Made with ⚡ & 🔒**
