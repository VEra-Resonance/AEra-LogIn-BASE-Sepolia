# VEra-Resonance v0.1 – Decentralized Proof-of-Human

A minimalist, wallet-based identity layer system that proves a user is a real human – **without KYC, without real names, without data sharing**.

---

## About VEra-Resonance

**VEra-Resonance** is a decentralized, privacy-preserving Proof-of-Human framework designed to protect digital spaces from bots, automated identities, synthetic engagement, and AI-generated fake accounts — without using KYC, biometrics, personal data, or centralized identity providers.

The system combines:

* **cryptographic wallet signatures**
* **behavioral on-chain pattern analysis**
* **a transparent Proof-of-Human score (0–100)**
* **non-tradable utility tokens for event logging**
* **zero personal data retention**
* **a resonance-based authenticity model**

VEra-Resonance aims to become a foundational standard for authenticity and human presence — applicable to social platforms, communities, decentralized networks and private ecosystems.

### 🔹 Core Principles

* **Anonymous but provably human**
* **No phone number, no email, no KYC**
* **Bot-resistant by design**
* **Privacy-first: no profiling, no tracking**
* **Interoperable with any platform (X, Discord, Web Apps)**
* **Zero speculation: the utility token has no market value**
* **Open, verifiable, cryptographically secure**

### 🔹 Mission

To restore **authenticity**, **trust** and **real human resonance**
in digital environments — through open, decentralized technology.

---

---

## 🎯 Features

✅ **Wallet Login** – MetaMask & WalletConnect Support  
✅ **Resonance Score** – Intelligent Scoring System (0–100)  
✅ **REST API** – Simple verification for other platforms  
✅ **SQLite Database** – Fast, local persistence  
✅ **Privacy-First** – Only wallet ID + score, no personal data  
✅ **Production-Ready** – CORS middleware, error handling, audit trail  

---

## 🚀 Quick Start

### 1. Requirements

```bash
# Python 3.9+ required
python --version

# Update pip
pip install --upgrade pip
```

### 2. Installation

```bash
# Navigate to project directory
cd /path/to/webside-wallet-login

# Install dependencies
pip install fastapi uvicorn

# (Optional) Using requirements.txt
pip install -r requirements.txt
```

### 3. Start Server

```bash
# Development mode with auto-reload
uvicorn server:app --reload --port 8000

# Or Production mode
uvicorn server:app --host 0.0.0.0 --port 8000
```

**Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
✓ Database initialized: /path/to/aera.db
🚀 VEra-Resonance Server started
```

### 4. Open in Browser

Navigate to: **http://localhost:8000**

---

## 📋 Workflow

1. **Connect Wallet** – Click button, approve MetaMask
2. **Verify** – Server checks address and calculates score
3. **Display Resonance Score** – User receives score (50–100)
4. **Login Token** – For integration with other platforms

---

📁 Project Structure

```
webside-wallet-login/
├── index.html          # Frontend (HTML + JavaScript)
├── server.py           # Backend (FastAPI)
├── aera.db             # SQLite Database
├── README.md           # This file
├── LICENSE             # Apache 2.0
└── requirements.txt    # Python Dependencies (optional)
```

---

## 🔌 API Endpoints

### `POST /api/verify`

Verifies a wallet address and updates the score.

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

Health check for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "service": "VEra-Resonance v0.1",
  "timestamp": 1700334000
}
```

---

### `GET /api/user/{address}`

Retrieves user data.

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

Public statistics.

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

Retrieves login events for a user (up to 50 most recent).

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

## 💾 Database Schema

### Table: `users`

| Column | Type | Description |
|--------|------|-------------|
| `address` | TEXT (PK) | Wallet address (Unique) |
| `first_seen` | INTEGER | Unix timestamp of first login |
| `last_login` | INTEGER | Unix timestamp of last login |
| `score` | INTEGER | Resonance Score (0–100) |
| `login_count` | INTEGER | Number of logins |
| `created_at` | TEXT | ISO timestamp of creation |

### Table: `events`

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER (PK) | Event ID |
| `address` | TEXT | Wallet address |
| `event_type` | TEXT | "signup" or "login" |
| `score_before` | INTEGER | Score before action |
| `score_after` | INTEGER | Score after action |
| `timestamp` | INTEGER | Unix timestamp |
| `created_at` | TEXT | ISO timestamp |

---

## 🎓 Resonance Score Logic

The score starts at **50** for new users and can increase up to **100**.

- **New User**: 50 points
- **Each Login**: +1 point (maximum 100)
- **Audit Trail**: All changes are logged in the `events` table

**Future Enhancements:**
- Community attestations (+5 per confirmation)
- Inactivity penalty (-1 per week without login)
- On-Chain Integration (token balance, governance votes)

---

## 🔐 Security & Privacy

✅ **No Personal Data** – Only wallet addresses stored  
✅ **Signature Verification** – (Coming in v0.2)  
✅ **Non-Transactional** – No gas consumption  
✅ **HTTPS Ready** – Production deployment with SSL  
✅ **Audit Trail** – All events logged  
✅ **CORS Protection** – Configurable per domain  

---

## 🚀 Integration with Other Platforms

### Example: Forum Integration

```javascript
// Forum checks login status
const response = await fetch('https://aera-login.example.com/api/user/0x742d...');
const user = await response.json();

if (user.resonance_score >= 50) {
  // User is verified → grant access
  allowForumAccess(user.address);
}
```

### Example: Discord Bot

```python
@discord.command()
async def verify(ctx):
    """Verification for Discord"""
    # Request wallet address
    address = await prompt_wallet(ctx)
    
    # Query AEra server
    response = requests.get(f'https://api.aera-login.com/api/user/{address}')
    user = response.json()
    
    if user.get('resonance_score', 0) >= 50:
        await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name='Verified'))
```

---

## 📝 Environment Variables

Optional (for Production):

```bash
# .env (create this file)
FASTAPI_ENV=production
DATABASE_URL=sqlite:///aera.db
CORS_ORIGINS=https://aera.example.com
LOG_LEVEL=info
```

---

## 🧪 Testing

### cURL Tests

```bash
# Health check
curl http://localhost:8000/api/health

# Verify user
curl -X POST http://localhost:8000/api/verify \
  -H "Content-Type: application/json" \
  -d '{"address":"0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE"}'

# Get user data
curl http://localhost:8000/api/user/0x742d35Cc6634C0532925a3b844Bc59e7e6d6e0dE

# Get statistics
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

### With Gunicorn + Nginx

```bash
# Install Gunicorn
pip install gunicorn

# Start server (4 workers)
gunicorn server:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### With Docker

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

## 📄 License

**Apache License 2.0**

```
Copyright 2025 Karlheinz Beismann
VEra-Resonance Project

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

**Full License:** https://www.apache.org/licenses/LICENSE-2.0

---

## 👤 Credits

- **Creator & Maintainer:** Karlheinz Beismann
- **Project:** VEra-Resonance — Decentralized Proof-of-Human Architecture
- **Framework:** FastAPI, ethers.js, Web3.py
- **Community:** VEra-Resonance Project

---

## 🤝 Support

Questions or bugs? Create an issue on GitHub or contact the maintainer.

---

**VEra-Resonance © 2025 Karlheinz Beismann**  
*Proving Humanity via Resonance – No KYC, No Identity Theft.*
